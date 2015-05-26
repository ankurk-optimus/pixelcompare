 (function() {
	var PixelCompareApp = angular.module('PixelCompareApp', ['ngRoute',
    'HomeModule','NavBar','NewProject', 'Tests']);

	// configure our routes
	PixelCompareApp.config(['$routeProvider', function($routeProvider) {

        function getProjects(HomeFactory){
            return HomeFactory.getProjects();
        }

        function getTestCases(TestsFactory,$route){
            return TestsFactory.getTestCases($route.current.params.project_name);
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

        .when('/tests/:project_name', {
            templateUrl: '/static/js/tests/tests.html',
            controller: 'TestsCtrl',
            resolve:{
                testCases:getTestCases
            }
        })

		.otherwise({
			redirectTo: '/404'
		});

	}]);
 })();
