
app.controller("ClientSaveUpdateController",['$scope',"HttpService","$location","$rootScope","$route","ShareDataService",function($scope,HttpService,$location,$rootScope,$route,ShareDataService){
  $scope.loginStatus = true;
  $scope.$parent.loginSuccess = true;
  $scope.clientSaveUpdate = function(action){
    var params = angular.copy($scope.client)
    var endPointName = action === "update" ? "updateClient" :"Clients";
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
  $scope.viewClients =  function(){
    $location.path("/clientList").search({})
  }
  $scope.resetForm = function(){
    $scope.showForm = true;
    $scope.success = false;
    $scope.failure = false;
  }
  $scope.resetForm();
  $scope.client={
    client_coupon:"",
    phone_number:""
  }
  if($route.current.params.addNewClient){
      $scope.addNewClient = true;
      $scope.editClient = false;
      $scope.client={
        client_coupon:"",
        phone_number:""
      }
    }else if($route.current.params.editClient){
      $scope.addNewClient = false;
      $scope.editClient = true;
      $scope.client = ShareDataService.getClient();
    }
}])