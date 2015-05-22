'use strict';

NavBar.controller('NavBarCtrl', ['$scope',
	'$location', '$localStorage',
	function($scope, $location, $localStorage) {
		$scope.newProject = function() {
			$location.path('/new_project');
		};
		$scope.projectsList = function() {
			$location.path('/');
		};
	}
]);
