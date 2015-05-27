'use strict';

Tests.controller('TestsCtrl', ['$scope',
	'$location',
	'$route',
	'testCases',
	'TestsFactory', 'Upload',
	function($scope, $location, $route, testCases, TestsFactory, Upload) {
		$scope.testCases = testCases.testcases;
		$scope.projectName = testCases.projectName;

		$scope.selected = {
			testCase: null,
			image: null,
		};

		$scope.modalParams = {
			showModal: false,
			urlToOpen: null
		};

		$scope.toggleModal = function(url) {
			$scope.modalParams.showModal = !$scope.modalParams.showModal;
			$scope.modalParams.urlToOpen = url;
		};

		$scope.imageUrl = null;
		$scope.error = null;

		console.log($scope.testCases);
		console.log($scope.projectName);

		$scope.selectTestCase = function(testCase) {

			// Clear current selected elements.
			if ($scope.selected.testCase != null) {
				$scope.selected.testCase.selected = false;

			}
			if ($scope.selected.image != null) {
				$scope.selected.image.selected = false;
			}

			// Select the new testcase.
			$scope.selected.testCase = testCase;
			$scope.selected.testCase.selected = true;

			// Select the first image from this testcase.
			if ($scope.selected.testCase.images != undefined &&
				$scope.selected.testCase.images != null &&
				$scope.selected.testCase.images.length > 0) {
				$scope.selected.image = $scope.selected.testCase.images[0];
				$scope.selected.image.selected = true;
			} else {
				$scope.selected.image = null;
			}

			$scope.error = null;
		};

		$scope.selectImage = function(image) {

			// Clear currently selected elements.
			if ($scope.selected.image != null) {
				$scope.selected.image.selected = false;
			}

			// Select the new element.
			$scope.selected.image = image;
			$scope.selected.image.selected = true;
			$scope.error = null;
		};

		$scope.compare = function() {
			if ($scope.selected.testCase == undefined || $scope.selected.testCase == null) {
				$scope.error = "Test case not selected.";
			} else if ($scope.selected.image == undefined || $scope.selected.image == null) {
				$scope.error = "Device not selected."
			}
			var pageName = $scope.selected.testCase.pageName;
			var device = $scope.selected.image.device;

			TestsFactory.compare($scope.projectName, pageName, device).then(function(response) {
				console.log(response);
				$scope.selected.image.output.contourOnSource = null;
				$scope.selected.image.output.contourOnSubject = null;
				$scope.selected.image.output.diff = null;
				setTimeout(function() {
					$scope.$apply(function() {
						$scope.selected.image.output.contourOnSource = response.contourOnSource;
						$scope.selected.image.output.contourOnSubject = response.contourOnSubject;
						$scope.selected.image.output.diff = response.diff;
					});
				}, 3000);

			}, function(error) {
				console.log(error);
				$scope.error = error.message;
			});
		};

		$scope.uploadSource = function(files) {
			if (files && files.length == 1) {
				var file = files[0];
				Upload.upload({
					method: 'POST',
					url: 'http://localhost:5000/upload/' + $scope.projectName,
					headers: {
						'Content-Type': 'application/json',
					},
					fileName: $scope.selected.image.device + '.png',
					file: file,
					fileFormDataName: 'file',
					fields: {
						type: 'source',
						pageName: $scope.selected.testCase.pageName,
						device: $scope.selected.image.device
					}
				}).progress(function(evt) {
					var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
					console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
				}).success(function(data, status, headers, config) {
					var response = data.data;
					console.log(response);
					$scope.selected.image.source = null;
					setTimeout(function(){
						$scope.$apply(function() {
							$scope.selected.image.source = response.path;
						});
					}, 3000);

				}).error(function() {
					$scope.error = "Image could not be uploaded.";
					$scope.selected.image.source = temp;
				});
			}
		};

		$scope.uploadScreenshot = function(files) {
			if (files && files.length == 1) {
				var file = files[0];
				Upload.upload({
					method: 'POST',
					url: 'http://localhost:5000/upload/' + $scope.projectName,
					headers: {
						'Content-Type': 'application/json',
					},
					fileName: $scope.selected.image.device + '.png',
					file: file,
					fileFormDataName: 'file',
					fields: {
						type: 'screenshots',
						pageName: $scope.selected.testCase.pageName,
						device: $scope.selected.image.device
					}
				}).progress(function(evt) {
					var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
					console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
				}).success(function(data, status, headers, config) {
					var response = data.data;
					console.log(response);
					$scope.selected.image.screenshot = null;
					setTimeout(function(){
						$scope.$apply(function() {
							$scope.selected.image.screenshot = response.path;
						});
					}, 3000);
				}).error(function() {
					$scope.error = "Image could not be uploaded.";
				});;
			}
		};

		// Check if we have testcases.
		if ($scope.testCases != undefined && $scope.testCases != null && $scope.testCases.length > 0) {
			$scope.selectTestCase($scope.testCases[0]);
		}
	}
]);
