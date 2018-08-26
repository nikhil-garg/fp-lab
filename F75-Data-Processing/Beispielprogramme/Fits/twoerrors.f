      PROGRAM MAIN
      IMPLICIT NONE
*
* Purpose: linear fit of data containing two quantities measured with errors
*
* Author : Victor Lendermann         Created at: 29.06.2005
*
* Calls  : CERNLIB MINUIT functions
*
* --- declare fit function
      EXTERNAL FCN
*
* --- declare parameter-, step-, startvalue-arrays
      integer NPAR
      parameter (NPAR=2)
      double precision VSTART(NPAR), VSTEP(NPAR)
      character*10 VNAM(2)
      data VNAM   /'Y/X-Slope ','Intercept '/
      data VSTART /-1D0,11D0/
      data VSTEP  /2*0.000001D0/
*
* --- declare command line argument strings
      character*32 argum
      integer narg
      real rargum
*
* --- declare argument-array for call to MNEXCM
      double precision ARGLIS(10)
*
* --- other variables
      integer i, ierr
*
* --- declare output variables
c      integer NPT, NFOUND
c      parameter (NPT=100)
c      double precision XPT(NPT), YPT(NPT)
*
* --- parse command line arguments
*
      narg = IARGC()
      if (narg.ge.3) then
         print*,'No more than 2 command line arguments are accepted.'
         print*,'These are initial values for Slope and Intercept.'
         print*,'Defaults: ',VSTART(1), VSTART(2)
         print*,'Values can only be given as FLOAT numbers: 12.0 ...'
         STOP
      endif
      if (narg.ge.1) then
         call GETARG(1,argum)
         call IZCTOR (argum,rargum)
         VSTART(1) = dble(rargum)
      endif
      if (narg.ge.2) then
         call GETARG(2,argum)
         call IZCTOR (argum,rargum)
         VSTART(2) = dble(rargum)
      endif
*
* --- initialize MINUIT units
      call MNINIT(5,6,7)
*
* --- specify title
      call MNSETI('Fit wit Errors in X and Y')
*
* --- define parameters for MINUIT
      do i = 1, NPAR
         call MNPARM(I,VNAM(I),VSTART(I),VSTEP(I),0.D0,0.D0,IERR)
         if (IERR.ne.0) STOP 'MAIN: mnparm failed'
      enddo
*
* --- set NOGRADIENT for MINUIT
      call MNEXCM(FCN,'SET NOG',ARGLIS,0,IERR,0)
      if (IERR.ne.0) STOP 'MAIN: set NOG failed'
*
* --- call FCN with IFLAG 1 to initialize
      ARGLIS(1)=1D0
      call MNEXCM(FCN,'CALL',ARGLIS,1,IERR,0)
      if (IERR.ne.0) then
         print*,'INITIAL PARAMETER SETTING FAILED. SOMETHING WENT WRONG'
         print*,'(call to FCN with IFLAG=1 failed)'
         STOP
      endif
*
* --- call MIGRAD
      call MNEXCM(FCN,'MIG',ARGLIS,0,IERR,0)
      if (IERR.ne.0) then
         print*,'MINIMIZATION FAILED !!! (migrad failed statement)'
         STOP
      endif
* --- call MNCONT
c      CALL MNCONT(FCN,1,2,NPT,XPT,YPT,NFOUND,0)
c      print*,'number of points on contour has to be ',NPT,NFOUND
* --- call CONtour
c      CALL MNEXCM(FCN,'CON',ARGLIS,0,IERR,0)
c      if (IERR.ne.0) STOP 'MAIN: contour failed'
*
      print*,' '
      print*,'DO THE RESULT VALUES LOOK REASONABLE?'
      print*,'Did you try to adjust initial parameter values?'
      print*,' '
*
* --- that's all
      END
*
*
      SUBROUTINE FCN(NPAR,GRAD,FVAL,XVAL,IFLAG,FUTIL)
      IMPLICIT NONE
*
* --- declaration of parameters
*     XVAL(1) : slope of the T(omega) straight line
*     XVAL(2) : axis intercept (Achsenabschnitt)
*
      integer NPAR,IFLAG
      double precision GRAD(*), XVAL(*), FVAL, FUTIL
*
* --- declaration of data arrays
*
      integer NDATA
      integer NDMAX
      parameter (NDMAX=10000)
      double precision X(NDMAX),EX(NDMAX)
      double precision Y(NDMAX),EY(NDMAX)
*
* --- other variables
*
      integer IOS, ic
      double precision xx, yy, exx, eyy, a, b
      
      save
*
* --- read input data
*
      if (IFLAG.eq.1) then
         NDATA = 0
 10      read(5,*,IOSTAT=IOS) xx, exx, yy, eyy
         if (IOS.eq.0) then
            NDATA = NDATA + 1
            X(NDATA)  = xx
            Y(NDATA)  = yy
            EX(NDATA) = exx
            EY(NDATA) = eyy
c           print*,x(ndata),ex(ndata),y(ndata),ey(ndata)
            if (NDATA.lt.NDMAX) then
               goto 10
            else
               print*,'FCN: too many points : ',NDMAX,' !!!!!!!'
            endif
         endif
         if (NDATA.eq.0) then
            print*,' '
            print*,'COULD NOT READ DATA FROM STANDARD INPUT !!!'
            print*,'Please, save your data in some file.'
            print*,'The file must include a table of 4 columns:'
            print*,'  X  Error_of_X  Y  Error_of_Y'
            print*,'Provide this file via standard input like:'
            print*,'  twoerrors.exec ARGUMENTS < FILENAME'
            print*,' '
            print*,'Up to 2 arguments can be specified.'
            print*,'These are initial values for Slope and Intercept.'
            print*,'See actual values above!'
            print*,'Values can only be given as FLOAT numbers: 12.0 ...'
            print*,' '
            STOP
         endif
         print*,NDATA,' data points read'
         RETURN
      endif
*
* --- calculate value to minimize
*
      FVAL = 0D0
      do ic=1, NDATA
         FVAL = FVAL + (Y(ic) - XVAL(1)*X(ic) - XVAL(2))**2 /
     $          (EY(ic)*EY(ic) + XVAL(1)*XVAL(1) * EX(ic)*EX(ic))
      enddo
c     print*,FVAL
*
      RETURN
      END
*
