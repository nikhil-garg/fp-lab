cmake_minimum_required(VERSION 2.8)
 
project(Aufgabe3_Registrierung)
 
find_package(ITK REQUIRED)
include(${ITK_USE_FILE})


add_executable(Aufgabe3_Registrierung MACOSX_BUNDLE  aufgabe3.cpp )
target_link_libraries(Aufgabe3_Registrierung ${ITK_LIBRARIES})