'use strict';

Tests.factory("TestsFactory", function($q, $http, $location, $rootScope) {

	var factory = {};

	factory.getTestCases = function(projectName) {
		var deferred = $q.defer();
		$http({
			method: 'GET',
			url: $rootScope.baseUrl + 'testcases/' + projectName,
			headers: {
				'Content-Type': 'application/json',
			},
			data: null
		}).then(function(result) {
			var data = result.data;
			if (data.error_code == 0) {
				deferred.resolve(data.data)
			} else {
				deferred.reject(data);
			}
		}, function(error) {
			deferred.reject(error);
		});
		return deferred.promise;
	};

	factory.compare = function(projectName, pageName, device){
		var deferred = $q.defer();
		$http({
			method: 'GET',
			url: $rootScope.baseUrl + 'compare/' + projectName + '/' + pageName + '/' + device,
			headers: {
				'Content-Type': 'application/json',
			},
			data: null
		}).then(function(result) {
			var data = result.data;
			if (data.error_code == 0) {
				deferred.resolve(data.data)
			} else {
				deferred.reject(data);
			}
		}, function(error) {
			deferred.reject(error);
		});
		return deferred.promise;
	};

	return factory;

})
