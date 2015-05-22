'use strict';

HomeModule.controller('HomeCtrl', ['$scope', 'projects',
	function($scope, projects) {
		$scope.projects = projects;
	}
]);
