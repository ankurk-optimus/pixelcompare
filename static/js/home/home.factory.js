'use strict';

HomeModule.factory("HomeFactory", function($q, $http, $location){

	var factory = {};

	factory.getProjects = function(){
		var deferred = $q.defer();
		$http({
            method: 'GET',
            url: 'http://localhost:5000/projects',
            headers: {
                'Content-Type': 'application/json',
            },
            data: null
        }).then(function(result) {
            var data = result.data;
            if (data.error_code == 0) {
            	var projects= data.data;
                deferred.resolve(projects);
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
