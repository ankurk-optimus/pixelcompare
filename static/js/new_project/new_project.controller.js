'use strict';

NewProject.controller('NewProjectCtrl', ['$scope', 'NewProjectFactory', '$location',

	function($scope, NewProjectFactory, $location) {

		var config = {
			"projectName": "Sample",
			"subject": [{
				"pageName": "Page 1",
				"pageUrl": "www.example.com",
				"devices": [
					"iOS",
					"Android"
				]
			}, {
				"pageName": "Page 2",
				"pageUrl": "www.example.com",
				"devices": [
					"iOS",
					"Android"
				]
			}, {
				"pageName": "Page 3",
				"pageUrl": "www.example.com",
				"devices": [
					"iOS",
					"Android"
				]
			}]
		};

		var devices = {
			"iOS": {
				"name": "iOS",
				"width": 320,
				"height": 480
			},
			"Android": {
				"name": "Android",
				"width": 320,
				"height": 480
			}
		};

		$scope.configSettings = {
			data: config,
			options: {
				mode: 'tree'
			}
		};
		$scope.devicesSettings = {
			data: devices,
			options: {
				mode: 'tree'
			}
		};

		$scope.error = null;

		$scope.projectName = "Sample";

		$scope.onLoad = function(instance) {
			instance.expandAll();
		};

		$scope.createProject = function() {
			$scope.error = null;
			if ($scope.projectName == null || $scope.projectName.length == 0)
				return;
			if ($scope.configSettings.data == null || $scope.devicesSettings.data == null)
				return;
			NewProjectFactory.createProject($scope.configSettings.data, $scope.devicesSettings.data).then(function(response) {
				console.log(response);
				$location.path("/")
			}, function(error) {
				console.log(error);
				$scope.error = "Project could not be created.";
			});
		};
	}
]);
