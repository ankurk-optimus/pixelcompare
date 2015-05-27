'use strict';

HomeModule.controller('HomeCtrl', ['$scope', 'projects', '$location',
	function($scope, projects, $location) {
		$scope.projects = projects;

		$scope.selectProject = function(project){
			$location.path('/tests/' + project)
		};
	}
]);
