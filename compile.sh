#
# Shell Script to automate Compilation and Running of C++ and Python scripts.
# Can be called by editors like Notepad++, Visual Studio Code.
#

print_usage()
{
	echo Usage: "compile[.sh] FileName (COMPILE|RUN|CPPCHECK) [targetName]"
	echo "'targetName' - name of the executable created or which executable to run"
	echo "               No extension is required"
	echo "               Default value = a"
}

run()
{
	case $extension in
		cpp)
			if ! [ -f $targetFile".exe" ]
			then
				echo $fullpath ":10:1: error" $targetFile".exe" "doesn't exist."
				exit 1
			fi
			start "" "/c/ExtLibs/cb_console_runner.exe" $targetFile
			;;
		py)
			start "" "/c/ExtLibs/cb_console_runner.exe" python $fullpath
			;;
		*)
			echo $extension "not implemented yet"
	esac
	echo Run Complete
}

compile()
{
	case $extension in
		cpp)
			local compileType=$(head -n 1 $fullpath)
			local includeoptions=""
			local linkeroptions=""
			
			case $compileType in
				"/*SFML*/")
					includeoptions="-IC:\ExtLibs\SFML-2.3\include"
					linkeroptions="-LC:\ExtLibs\SFML-2.3\lib -lsfml-audio -lsfml-network -lsfml-graphics -lsfml-window -lsfml-system"
					;;
				"/*OPENGL*/")
					includeoptions="-IC:\ExtLibs\SFML-2.3\include -IC:\ExtLibs\glew-1.12.0\include"
					linkeroptions="-LC:\ExtLibs\SFML-2.3\lib -LC:\ExtLibs\glew-1.12.0\lib -lsfml-audio -lsfml-network -lsfml-graphics -lsfml-window -lsfml-system -lGLU32 -lGLEW32 -lopengl32"
					;;
			esac
			
			if [ -f $targetFile".exe" ]
			then
				rm $targetFile".exe"
			fi
			if [ -f $targetFile".o" ]
			then
				rm $targetFile".o"
			fi
			
			g++ -g -Wunreachable-code -std=c++11 -pedantic -Wextra -Wall $includeoptions -c "$fullpath" -o $targetFile".o"
			
			if [ $? -ne 0 ]
			then
				echo Compilation Failed
				exit 1
			fi
			
			g++.exe -o $targetFile".exe" $targetFile".o" $linkeroptions
			
			if [ $? -ne 0 ]
			then
				echo Compilation Failed
				exit 1
			fi
			
			;;
		# java)
			# start "" "/c/ExtLibs/cb_console_runner.exe" %JAVA_HOME%/bin/javac -cp %CP% "$filename"
			# ;;
		py)
			start "" "/c/ExtLibs/cb_console_runner.exe" python $fullpath
			;;
		*)
			echo $extension "not implemented yet"
	esac
	echo Compilation Complete
}

if [ $# -ne 2 ] && [ $# -ne 3 ]
then
	echo ERROR: Wrong number of arguments
	print_usage
	exit 1
fi

if ! [ -f "$1" ]
then
	echo 'ERROR: "'$1'"' "doesn't exits"
	exit 1
fi

if [ $2 != "COMPILE" ] && [ $2 != "RUN" ] && [ $2 != "CPPCHECK" ]
then
	echo "ERROR: '"$2"'" "is not a valid Command"
	print_usage
	exit 1
fi

if [ $# -eq 3 ]
then
	targetFile=$3
else
	targetFile="/g/work/c++_progs/a"
fi

fullpath=$1
extension=$([[ "$1" = *.* ]] && echo "${1##*.}" || echo '')

if [ -z $extension ]
then
	echo "No idea what to do with file with ''(null) extension."
	exit 1
fi

case $2 in
	RUN)
		run
		;;
	COMPILE)
		"/g/Program Files/Cppcheck/cppcheck.exe" --enable=all $fullpath
		compile
		;;
esac
exit 0
