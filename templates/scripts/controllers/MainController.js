
app.controller("MainController",['$scope',"HttpService","$location","$rootScope",function($scope,HttpService,$location,$rootScope){
  $scope.loginStatus = true;
  $scope.loginSuccess = false;
  $scope.goto = function(path){
    var searchParams = {
      addNewClient:null,
      addNewTemplate:null,
      editClient:null,
      editTemplate:null
    }
    $location.path("/"+path).search({});
  }
}])