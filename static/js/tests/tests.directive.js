Tests.directive("fullHeightPanel",function($window){
	return {
		restrict: 'A',
		scope :{
			offset:"="
		},
		link:function(scope, element, attrs){
			element.height($(window).height() - scope.offset);
		}
	};
});
