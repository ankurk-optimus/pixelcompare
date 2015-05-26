'use strict';

Tests.controller('TestsCtrl', ['$scope',
	'$location',
	'$route',
	'testCases',
	function($scope, $location, $route, testCases) {
		$scope.testCases = testCases.testcases;
		$scope.projectName = testCases.projectName;

		$scope.selected = {
			testCase: null,
			image: null,
		};

		console.log($scope.testCases);
		console.log($scope.projectName);

		$scope.selectTestCase = function(testCase) {

			// Clear current selected elements.
			if ($scope.selected.testCase != null) {
				$scope.selected.testCase.selected = false;

			}
			if($scope.selected.image!=null){
				$scope.selected.image.selected=false;
			}

			// Select the new testcase.
			$scope.selected.testCase = testCase;
			$scope.selected.testCase.selected = true;

			// Select the first image from this testcase.
			if ($scope.selected.testCase.images != undefined &&
				$scope.selected.testCase.images != null &&
				$scope.selected.testCase.images.length > 0) {
				$scope.selected.image = $scope.selected.testCase.images[0];
				$scope.selected.image.selected=true;
			} else {
				$scope.selected.image = null;
			}
		};

		$scope.selectImage = function(image) {

			// Clear currently selected elements.
			if($scope.selected.image!=null){
				$scope.selected.image.selected=false;
			}

			// Select the new element.
			$scope.selected.image = image;
			$scope.selected.image.selected=true;
		};

		// Check if we have testcases.
		if($scope.testCases!=undefined && $scope.testCases!=null && $scope.testCases.length>0){
			$scope.selectTestCase($scope.testCases[0]);
		}
	}
]);
