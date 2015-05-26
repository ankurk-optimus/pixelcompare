Tests.directive("listItem", function(){
	return {
		scope:{
			testCase:"="
		},
		replace:true,
		restrict:"E",
		templateUrl:"static/js/tests/testcase_listitem/list_item.html",
		controller:"ListItemCtrl"
	}
});
