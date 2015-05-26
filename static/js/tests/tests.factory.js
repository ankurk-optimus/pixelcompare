'use strict';

Tests.factory("TestsFactory", function($q, $http, $location) {

	var factory = {};

	factory.getTestCases = function(projectName) {
		var deferred = $q.defer();
		$http({
			method: 'GET',
			url: 'http://localhost:5000/testcases/' + projectName,
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
