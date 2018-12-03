// itk includes
#include "itkImageRegistrationMethodv4.h"
#include "itkMattesMutualInformationImageToImageMetricv4.h"
#include "itkVersorRigid3DTransform.h"
#include "itkQuasiNewtonOptimizerv4.h"
#include "itkTimeProbe.h"
#include "itkCommand.h"

// function collection includes
#include "nrnGlobals.h"

// system includes
#include <sys/stat.h>
#include <fstream>
#include <stdlib.h>  
#include <iostream>
#include <iomanip>


// zur Anzeige der Iterationen während der Optimierung:
class CommandIterationUpdate : public itk::Command
{
public:
	typedef  CommandIterationUpdate   Self;
	typedef  itk::Command             Superclass;
	typedef itk::SmartPointer<Self>   Pointer;
	itkNewMacro(Self);

protected:
	CommandIterationUpdate() {};

public:
	typedef itk::QuasiNewtonOptimizerv4  OptimizerType;
	typedef   const OptimizerType *                             OptimizerPointer;
	void Execute(itk::Object *caller, const itk::EventObject & event) ITK_OVERRIDE
	{
		Execute((const itk::Object *)caller, event);
	}
	void Execute(const itk::Object * object, const itk::EventObject & event) ITK_OVERRIDE
	{
		OptimizerPointer optimizer = static_cast< OptimizerPointer >(object);
		if (!itk::IterationEvent().CheckEvent(&event))
		{
			return;
		}
		std::cout << optimizer->GetCurrentIteration() << "   ";
		std::cout << optimizer->GetValue() << "   ";
		std::cout << optimizer->GetCurrentPosition() << std::endl;
	}
};


int main( int argc, char *argv[] )
{
	const unsigned int                          Dimension = 3;
	typedef  double                           PixelType;

	
   
	unsigned int histBins = 50;
	
  // load data:	
	typedef itk::Image< double, 3 >         ImageType;
	ImageType::Pointer fixedImage = nrnLoadImage<ImageType>
									("C:/FP/Allgemein/Daten/patient_106/ct/patient_106_ct.mhd");
	ImageType::Pointer movingImage = nrnLoadImage<ImageType>
								("C:/FP/Allgemein/Daten/patient_106/mr_T2/patient_106_mr_T2.mhd");

  // define transform:
	typedef itk::VersorRigid3DTransform<double> TransformType;
	TransformType::Pointer transform = TransformType::New();
	typedef itk::Image< PixelType, Dimension >  FixedImageType;
	typedef itk::Image< PixelType, Dimension >  MovingImageType;
  // define optimizer and metric:
	typedef itk::QuasiNewtonOptimizerv4  OptimizerType;
	typedef itk::MattesMutualInformationImageToImageMetricv4<
											FixedImageType,
											MovingImageType >   MetricType;
	typedef itk::ImageRegistrationMethodv4<
										  FixedImageType,
										  MovingImageType,
										  TransformType >	RegistrationType;

	MetricType::Pointer         metric        = MetricType::New();
	OptimizerType::Pointer      optimizer     = OptimizerType::New();
	RegistrationType::Pointer   registration  = RegistrationType::New();
	
	metric->SetNumberOfHistogramBins(histBins);
	registration->SetMetric(        metric        );
	registration->SetOptimizer(     optimizer     );
	registration->SetFixedImage(    fixedImage );
	registration->SetMovingImage(   movingImage  );
	registration->SetInitialTransform( transform );
	double Pixel = fixedImage->GetLargestPossibleRegion().GetNumberOfPixels();
	typedef itk::RegistrationParameterScalesFromPhysicalShift< MetricType > 
									RegistrationParameterScalesFromShiftType;
	RegistrationParameterScalesFromShiftType::Pointer shiftScaleEstimator 
							= RegistrationParameterScalesFromShiftType::New();
	shiftScaleEstimator->SetMetric(metric);
	optimizer->SetMetric( metric );
	optimizer->SetMaximumIterationsWithoutProgress(50);
	optimizer->SetNumberOfIterations( 500 );
	optimizer->SetScalesEstimator( shiftScaleEstimator );
	optimizer->SetConvergenceWindowSize(50);
	optimizer->ReturnBestParametersAndValueOn();

	CommandIterationUpdate::Pointer observer = CommandIterationUpdate::New();
	optimizer->AddObserver(itk::IterationEvent(), observer);
  // multi Resolution:
	RegistrationType::ShrinkFactorsArrayType shrinkFactorsPerLevel;
	RegistrationType::SmoothingSigmasArrayType smoothingSigmasPerLevel;
	
	/*
	unsigned int numberOfLevels = 1;
	shrinkFactorsPerLevel.SetSize(numberOfLevels);
	shrinkFactorsPerLevel[0] = 1;

	smoothingSigmasPerLevel.SetSize(numberOfLevels);
	smoothingSigmasPerLevel[0] = 0;
	*/
	
	unsigned int numberOfLevels = 4;
	shrinkFactorsPerLevel.SetSize(numberOfLevels);
	shrinkFactorsPerLevel[0] = 4;
	shrinkFactorsPerLevel[1] = 3;
	shrinkFactorsPerLevel[2] = 2;
	shrinkFactorsPerLevel[3] = 1;
	
	smoothingSigmasPerLevel.SetSize(numberOfLevels);
	smoothingSigmasPerLevel[0] = 2;
	smoothingSigmasPerLevel[1] = 1;
	smoothingSigmasPerLevel[2] = 0;
	

	registration->SetNumberOfLevels( numberOfLevels );
	registration->SetSmoothingSigmasPerLevel( smoothingSigmasPerLevel );
	registration->SetShrinkFactorsPerLevel( shrinkFactorsPerLevel );
	

	double samplingPercentage = 0.4;
	RegistrationType::MetricSamplingStrategyType  samplingStrategy 
												=  RegistrationType::RANDOM;
	registration->SetMetricSamplingPercentage( samplingPercentage );
	registration->SetMetricSamplingStrategy(samplingStrategy);


	double optTime;
	try
	{
		itk::TimeProbe clock;
		clock.Start();
 		registration->Update();
		clock.Stop();
		optTime = clock.GetTotal();
		std::cout << "Time: "<< optTime << "\n";
	}
	catch( itk::ExceptionObject & err )
	{
		std::cerr << "ExceptionObject caught !" << std::endl;
		std::cerr << err << std::endl;
		return EXIT_FAILURE;
	}

  const TransformType::ParametersType finalParameters =
                            registration->GetOutput()->Get()->GetParameters();

  const double versorX              = finalParameters[0];
  const double versorY              = finalParameters[1];
  const double versorZ              = finalParameters[2];
  const double finalTranslationX    = finalParameters[3];
  const double finalTranslationY    = finalParameters[4];
  const double finalTranslationZ    = finalParameters[5];
  const unsigned int numberOfIterations = optimizer->GetCurrentIteration();
  const double bestValue = optimizer->GetValue();

  TransformType::Pointer finalTransform = TransformType::New();

  finalTransform->SetFixedParameters
					( registration->GetOutput()->Get()->GetFixedParameters() );
  finalTransform->SetParameters( finalParameters );
  
  ImageType::Pointer resampledImage = resampleImage<ImageType,TransformType>
										(movingImage,fixedImage,finalTransform);

  nrnSaveImage<ImageType>("20patient6.mhd", resampledImage);

  // Analysis (only for Training!):
  typedef itk::PointSet< double, 3 >   PointSetType;
  PointSetType::Pointer fixedLandmarks = nrnLoadLandmarks<PointSetType>("C:/FP/Allgemein/Daten/training_001/transform/landmarks_ct.txt");
  PointSetType::Pointer movingLandmarks = nrnLoadLandmarks<PointSetType>("C:/FP/Allgemein/Daten/training_001/transform/landmarks_mrT2.txt");
  TransformType::Pointer transform2 = markerbasedRegistration<ImageType,PointSetType,TransformType>(fixedLandmarks,movingLandmarks,fixedImage);

  // registration error:
  double regError= getRegistrationError<ImageType,TransformType>(resampledImage,finalTransform,transform2);
  std::cout << "registration error (only for training!) [mm]: " << regError << "\n";
 
  // write output file:
    struct stat buffer; 
	bool fileExists = (stat ("output.txt", &buffer) == 0) ;

	std::string out = "output.txt";
	std::ofstream outputfile;
	outputfile.open(out.c_str(),std::ofstream::app);
	
	
	if (!fileExists)
		outputfile << "MI OptTime H \n";
	
	outputfile  << bestValue << " "
				<< optTime << " "
				<< histBins << " "
				<<"\n";
	outputfile.close();

  return EXIT_SUCCESS;
}