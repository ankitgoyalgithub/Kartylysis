
app.controller("ClientListController",['$scope',"HttpService","$location","$rootScope","$route","ShareDataService",function($scope,HttpService,$location,$rootScope,$route,ShareDataService){
  $scope.loginStatus = true;
  $scope.$parent.loginSuccess = true;
  
    $scope.getNumber = function(num) {
        return new Array(num);   
    }
    $scope.getClients = function(offset) {
      var params = {
        limit:8,
        offset:8*offset
      }
      HttpService("Clients").GET(params,function(response){
        var data = response.data
        $scope.totalPages = Math.ceil(data.count/8)
        $scope.clients = data.results;
      },function(data){
        console.log(data)
      });
    }
    $scope.getClients(0);

    $scope.getRegisteredCount = function(offset) {
      var params = {

      }
      HttpService("/getRegisteredCount").GET(params,function(response){
        var data = response.data
        $scope.totalPages = Math.ceil(data.count/8)
        $scope.clients = data.results;
      },function(data){
        console.log(data)
      });
    }

    $scope.clientSaveUpdate = function(action){
      var searchParams = {}
      if(action==="edit"){
        searchParams.addNewClient = false;
        searchParams.editClient = true;
      }
      else{
        searchParams.addNewClient = true;
        searchParams.editClient = false;
      }
      $location.path("/clientSaveUpdate").search(searchParams);
    }
    $scope.deleteClient = function(id,offset){
      HttpService("Clients").DELETE(id,function(response){
        $route.reload()
      },function(data){
        console.log(data)
      });
    }

    $scope.editClient = function (client) {
      ShareDataService.setClient(client);
      $scope.clientSaveUpdate("edit");
    }
}])