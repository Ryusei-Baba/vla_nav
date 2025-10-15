cmake_minimum_required(VERSION 3.8)
project(vla_nav)

## Create .git reference in build directory to fix setuptools-scm warning
set(GIT_DIR_PATH "${CMAKE_SOURCE_DIR}/../.git/modules/vla_nav")
if(EXISTS "${GIT_DIR_PATH}")
    file(WRITE "${CMAKE_BINARY_DIR}/.git" "gitdir: ${GIT_DIR_PATH}\n")
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(PROGRAMS
  vla_nav/vla_nav_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME vla_nav_node
)

# Install launch files
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
)

# Install config files
install(DIRECTORY
  config
  DESTINATION share/${PROJECT_NAME}/
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
