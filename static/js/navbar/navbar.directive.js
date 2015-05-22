"use strict";

NavBar.directive('navbar', function(){
  return{
    restrict: 'E',
    templateUrl: '/static/js/navbar/navbar.html',
    controller: 'NavBarCtrl',
    controllerAs: 'navbarCtrl'
  };
});
