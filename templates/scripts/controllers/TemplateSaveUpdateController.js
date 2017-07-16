
app.controller("TemplateSaveUpdateController",['$scope',"HttpService","$location","$rootScope","$route","ShareDataService",function($scope,HttpService,$location,$rootScope,$route,ShareDataService){
  $scope.loginStatus = true;
  $scope.$parent.loginSuccess = true;
  $scope.templateSaveUpdate = function (action){
    var params = angular.copy($scope.template)
    var endPointName = action === "update" ? "updateTemplate" :"Templates";
    HttpService(endPointName).POST(params,function(data){
        $scope.success = true;
        $scope.showForm = false;
      },
      function(data) {
        console.log("Error",data)
        $scope.failure = true;
        $scope.showForm = false;
    })
  }
  $scope.viewTemplate =  function(){
    $location.path("/viewTemplate").search({})
  }
  $scope.resetForm = function(){
    $scope.showForm = true;
    $scope.success = false;
    $scope.failure = false;
  }
  $scope.resetForm();
  $scope.template={
    company_name:"",
    sender_title:"",
    template_body:""
  }
  if($route.current.params.addNewTemplate){
      $scope.addNewTemplate = true;
      $scope.editTemplate = false;
      $scope.template={
        company_name:"",
        sender_title:"",
        template_body:""
      }
    }else if($route.current.params.editTemplate){
      $scope.addNewTemplate = false;
      $scope.editTemplate = true;
      $scope.template = ShareDataService.getTemplate();
    }
}])