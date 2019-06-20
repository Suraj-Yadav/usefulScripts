/* watch -- execute a program repeatedly, displaying output fullscreen
 *
 * Based on watch present in procps. 
 * Written for Windows as couldn't find a better watch command.
 * 
 * Requires Boost::Program_options and Boost::filesystem
 * Compilation command (MINGW):
 * 		g++ -std=c++17 watch.cpp -l boost_program_options -l wsock32 -l boost_system -l boost_filesystem
 */

#define DEFINE_CONSOLEV2_PROPERTIES

#include <cstdio>
#include <cstdlib>
#include <iostream>

#include <boost/process.hpp>
#include <boost/program_options.hpp>

// System headers
#include <windows.h>
#ifndef ENABLE_VIRTUAL_TERMINAL_PROCESSING
#define ENABLE_VIRTUAL_TERMINAL_PROCESSING 0x0004
#endif

#define ESC "\x1b"
#define CSI "\x1b["

namespace po = boost::program_options;

bool EnableVTMode(HANDLE& hOut) {
	DWORD dwMode = 0;
	if (!GetConsoleMode(hOut, &dwMode)) {
		return false;
	}

	dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
	if (!SetConsoleMode(hOut, dwMode)) {
		return false;
	}
	return true;
}

std::pair<int, int> getConsoleSize(HANDLE& hOut) {
	CONSOLE_SCREEN_BUFFER_INFO ScreenBufferInfo;
	GetConsoleScreenBufferInfo(hOut, &ScreenBufferInfo);
	COORD Size;
	return {ScreenBufferInfo.srWindow.Right - ScreenBufferInfo.srWindow.Left + 1,
			ScreenBufferInfo.srWindow.Bottom - ScreenBufferInfo.srWindow.Top + 1};
}

void moveCursor(HANDLE& hOut, int x, int y) {
	COORD destination;
	destination.X = x;
	destination.Y = y;
	SetConsoleCursorPosition(hOut, destination);
}

bool done = false;

void die(int signum) {
	std::cout << "Interrupt signal (" << signum << ") received.\n";
	done = true;
}

void watch(const std::string& command, double interval, bool noTitle) {
	HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
	if (hOut == INVALID_HANDLE_VALUE) {
		std::cout << "Couldn't get the console handle. Quitting.\n";
		return;
	}

	//First, enable VT mode
	bool fSuccess = EnableVTMode(hOut);
	if (!fSuccess) {
		std::cout << "Unable to enter VT processing mode. Quitting.\n";
		return;
	}

	signal(SIGINT, die);
	signal(SIGTERM, die);

	auto p = boost::process::search_path("bash");

	DWORD dwMode = 0;

	auto [oldWidth, oldHeight] = getConsoleSize(hOut);

	// Enter the alternate buffer
	std::cout << CSI "?1049h" << CSI "?25l";

	while (!done) {
		boost::process::ipstream is;  //reading pipe-stream
		int retCode;
		try {
			retCode = boost::process::system(p, "-c", command, boost::process::std_out > is, boost::process::std_err > stderr);
		}
		catch (const std::exception& e) {
			std::cerr << "Exception Occurred" << e.what() << '\n';
			break;
		}

		if (done) break;

		const auto [width, height] = getConsoleSize(hOut);

		if (oldWidth > width) {
			moveCursor(hOut, 0, 0);
			std::cout << std::string(width * oldHeight, ' ');
			// done = true;
		}
		oldWidth = width;
		oldHeight = height;

		if (done) break;

		moveCursor(hOut, 0, 0);

		std::vector<std::string> data;

		std::string line;

		if (!noTitle) {
			char buff[1000];
			std::snprintf(buff, 1000, "Every %.1fs: %s", interval, command.c_str());
			std::string left(buff);
			std::time_t time = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());
			std::string timeStr(std::ctime(&time));
			timeStr.pop_back();
			if (left.size() + timeStr.size() + 2 > width) {
				size_t mid = 2, leftWidth = (width - 2) / 2 - 3, rightWidth = (width - 2) / 2 - 3;
				left = left.substr(0, leftWidth) + (leftWidth >= left.size() ? "" : "...");
				timeStr = timeStr.substr(0, rightWidth) + (rightWidth >= timeStr.size() ? "" : "...");
			}
			std::cout << left << std::string(width - (left.size() + timeStr.size()), ' ') << timeStr;
		}

		for (int lineNo = 2; lineNo < height && std::getline(is, line) && !line.empty(); lineNo++) {
			line.erase(std::find_if(line.rbegin(), line.rend(), [](int ch) { return !std::isspace(ch); }).base(), line.end());
			if (line.size() > width) {
				line = line.substr(0, width - 3) + "..\n";
			}
			else {
				line += std::string(width - line.size() - 1, ' ') + "\n";
			}
			std::cout << line;
		}

		if (done) break;
		Sleep(interval * 1000);
	}

	EnableVTMode(hOut);
	// Exit the alternate buffer
	std::cout << CSI "?1049l" << CSI "?25h";
}

int main(int argc, char* argv[]) {
	po::options_description desc("Allowed options");
	double interval;
	bool noTitle = false;
	std::string usage("Usage: watch [options] <command>\n");

	// clang-format off
	desc.add_options()
		("help,h", "print a summary of the options")
		("version,v", "print the version number")
		("no-title,t", "turns off showing the header")
		("interval,n", po::value<double>(&interval)->default_value(2), "seconds to wait between updates")
		("command", po::value<std::string>(),"command to run");
	// clang-format on

	po::positional_options_description p;
	p.add("command", 1);

	po::variables_map vm;
	try {
		po::store(po::command_line_parser(argc, argv).options(desc).positional(p).run(), vm);
		po::notify(vm);
	}
	catch (const std::exception& e) {
		std::cerr << e.what() << '\n';
	}

	if (vm.count("help")) {
		std::cout << usage << desc << "\n";
		return 0;
	}
	else if (vm.count("version")) {
		std::cout << "watch 0.0.0\n";
		return 0;
	}
	else if (!vm.count("command")) {
		std::cerr << "Incorrect Usage.\nExpected " << usage << "See 'watch -h' for more";
		return -1;
	}

	try {
		auto command = vm["command"].as<std::string>();
		interval = std::max(interval, 0.1);
		noTitle = vm.count("no-title");
		watch(command, interval, noTitle);
	}
	catch (const std::exception& e) {
		std::cerr << "Exception Occurred" << e.what() << '\n';
	}

	return 0;
}
