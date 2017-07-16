
app.controller("ViewTemplateController",['$scope',"HttpService","$location","$rootScope","ShareDataService","$route",function($scope,HttpService,$location,$rootScope,ShareDataService,$route){
  $scope.loginStatus = true;
  $scope.$parent.loginSuccess = true;
  
  $scope.getNumber = function(num) {
        return new Array(num);   
    }
    $scope.getTemplate = function(offset) {
      var params = {
        limit:8,
        offset:8*offset
      }
      HttpService("Templates").GET(params,function(response){
        var data = response.data
        $scope.totalPages = Math.ceil(data.count/8)
        $scope.templates = data.results;
      },function(data){
        console.log(data)

      });
    }
    $scope.getTemplate(0);
    $scope.templateSaveUpdate = function(action){
      var searchParams = {}
      if(action==="edit"){
        searchParams.addNewTemplate = false;
        searchParams.editTemplate = true;
      }
      else{
        searchParams.addNewTemplate = true;
        searchParams.editTemplate = false;
      }
      $location.path("/templateSaveUpdate").search(searchParams);
    }
    $scope.deleteTemplate = function(id,offset){
      var params = {
        id:id
      }
      HttpService("deleteTemplate").POST(params,function(response){
        $route.reload()
      },function(data){
        console.log(data)
      });
    }

    $scope.editTemplate = function (template) {
      ShareDataService.setTemplate(template);
      $scope.templateSaveUpdate("edit");
    }
}])