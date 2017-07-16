app.service("HttpService",['$http',function($http){
  return function(endpointName) {
    var baseURL = "http://ec2-35-166-47-143.us-west-2.compute.amazonaws.com:8000/";
    return {
      GET: function(params, successCallback, errorCallback) {
        var url = baseURL+endpointName+"/";
        var config;
        config = {
          params: params
        };
        return $http.get(url, config).then(successCallback, errorCallback);
      },
      POST: function(params, successCallback, errorCallback) {
        var url =  baseURL+endpointName+"/";
        var data = params
        var config= {
          headers:{
            "Content-Type":"application/json"
          }
        };
        return $http.post(url,data, config).then(successCallback, errorCallback);
      },
      DELETE: function(params, successCallback, errorCallback) {
        var url =  baseURL+endpointName+"/"+params+"/";
        var config= {
          headers:{
            "Content-Type":"application/json"
          }
        };
        return $http.delete(url,config).then(successCallback, errorCallback);
      }
    };
  };
}
]);
