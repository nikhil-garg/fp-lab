cmake_minimum_required(VERSION 2.8)
 
project(Aufgabe2)
 
find_package(ITK REQUIRED)
include(${ITK_USE_FILE})


add_executable(Aufgabe2 MACOSX_BUNDLE  aufgabe2.cpp )
target_link_libraries(Aufgabe2 ${ITK_LIBRARIES})