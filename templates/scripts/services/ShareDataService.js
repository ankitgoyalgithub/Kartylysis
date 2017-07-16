app.service('ShareDataService', function(){
  var data = {
    client:{
      client_id:"",
      client_coupon:"",
      phone_number:""
    },
    template:{
      id:"",
      company_name:"",
      sender_title:"",
      template_body:""
    }
  };
  return {
    setClient: function(client){
      data.client = client;
    },
    getClient:function(){
      return data.client;
    },
    setTemplate: function(template){
      data.template = template;
    },
    getTemplate:function(){
      return data.template;
    }
  }
})