@echo off
echo "Downloading JDK 8u73 ..."
wget.exe --no-cookies --no-check-certificate --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u73-b02/jdk-8u73-windows-x64.exe -O ..\SDK\jdk-8u73-windows-x64.exe
echo "Downloading Apache ANT ..."
wget.exe http://apache-mirror.rbc.ru/pub/apache//ant/binaries/apache-ant-1.9.7-bin.zip -O ..\SDK\apache-ant.zip
echo "Downloading Android NDK ..."
wget.exe http://dl.google.com/android/ndk/android-ndk-r9d-windows-x86_64.zip -O ..\SDK\android-ndk.zip
echo "Downloading Android SDK ..."
wget.exe --no-cookies --no-check-certificate https://dl.google.com/android/android-sdk_r24.4.1-windows.zip -O ..\SDK\android-sdk.zip
cd ..\SDK
echo "Installing JDK 8u73 ..."
jdk-8u73-windows-x64.exe /s INSTALLDIR="%CD%\jdk-8u73"
del /Q jdk-8u73-windows-x64.exe
echo "Installing Apache ANT ..."
%CD%\jdk-8u73\bin\jar.exe xfv apache-ant.zip
del /Q apache-ant.zip
echo "Installing Android NDK ..."
%CD%\jdk-8u73\bin\jar.exe xfv android-ndk.zip
del /Q android-ndk.zip
echo "Installing Android SDK ..."
%CD%\jdk-8u73\bin\jar.exe xfv android-sdk.zip
del /Q android-sdk.zip
%WINDIR%/system32/taskkill /f /im java.exe
set JAVA_HOME=%CD%\jdk-8u73
set ANT_HOME=%CD%\apache-ant-1.9.7
set ANDROID_NDK=%CD%\android-ndk-r9d
set ANDROID_SDK=%CD%\android-sdk-windows
set ANDROID_HOME=%CD%\android-sdk-windows
set ANDROID_SWT=%ANDROID_SDK%\tools\lib\x86
set PATH=%PATH%;%CD%\..\tools;%JAVA_HOME%;%ANDROID_SDK%\tools;%ANDROID_NDK%;%ANT_HOME%\bin
%CD%\android-sdk-windows\tools\android.bat update sdk -u -t 1,2,3,5,11,16,22,35
