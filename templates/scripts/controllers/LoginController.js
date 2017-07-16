
app.controller("LoginController",['$scope',"HttpService","$location","$rootScope",function($scope,HttpService,$location,$rootScope){
  $scope.loginStatus = true;
  $scope.$parent.loginSuccess = false;
  $scope.login = function (){
    var params = {
      username:$scope.uname,
      password:$scope.psw
    }
    HttpService("validateAdmin").POST(params,function(data){
        if(data.data.isValidUser){
          $location.path("/clientList");
          $scope.$parent.loginSuccess = true;
        }
      },
      function(data) {
        console.log("Error",data)
    })
  }

}])