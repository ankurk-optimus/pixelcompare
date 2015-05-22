 (function() {
	var PixelCompareApp = angular.module('PixelCompareApp', ['ngRoute','HomeModule','NavBar','NewProject']);

	// configure our routes
	PixelCompareApp.config(['$routeProvider', function($routeProvider) {

        function getProjects(HomeFactory){
            return HomeFactory.getProjects();
        }

		$routeProvider

		// route for the home page
		.when('/', {
			templateUrl: '/static/js/home/home.html',
			controller: 'HomeCtrl',
            resolve:{
                projects:getProjects
            }
		})

        .when('/new_project', {
            templateUrl: '/static/js/new_project/new_project.html',
            controller: 'NewProjectCtrl'
        })

		.otherwise({
			redirectTo: '/404'
		});

	}]);
 })();
