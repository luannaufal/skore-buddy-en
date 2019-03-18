const functions = require('firebase-functions');
const { Logging } = require('@google-cloud/logging');
const rp = require('request-promise-native');
const {dialogflow,Suggestions,LinkOutSuggestion, List, SimpleResponse} = require('actions-on-google');

const MATERIALS = 'Materials';

const app = dialogflow();
const logging = new Logging();
const log = logging.log("luan-log");
const METADATA = {
  resource: {
    type: 'cloud_function',
    labels: {
      function_name: 'DialogFlow testing',
      region: 'us-central1'
    }
  }
};

function requestLoginSkore(){
  var options = {
    uri: "https://knowledge.skore.io/workspace/v3/login",
    method: "POST",
    body: {
      email: "luan.naufal@gmail.com",
      password: "PASSWORD",
      company_id: "5704"
    },
    headers: {
        "Content-type": "application/json",
		"Accept": "text/plain"
    },
    json: true,
    transform: function(body, response){
    	return body.token;
	},
  };
  return rp( options );
}

function requestMaterialsSkore(token){
  var options = {
    uri: "https://knowledge.skore.io/workspace/v2/spaces/34137/contents",
    headers: {
        "Content-type": "application/json",
		"Accept": "text/plain",
      	"Authorization": token
    },
    json: true,
    transform: function(body, response){
    	var output = [];
    	body.results.forEach(element => {
    		output.push(element.name);
    	});
    	console.log(output);
    	return output;
	},
  };
  return rp( options );
}

app.intent(MATERIALS, (conv) => {
	return requestLoginSkore()
  	.then( body => {
        log.write(log.entry(METADATA, {message: "Login output"}));
        return requestMaterialsSkore(body)
      	.then( materials => {
            log.write(log.entry(METADATA, {message: "Gettings materials output"}));
            log.write(log.entry(METADATA, {message: materials}));
            conv.ask(new SimpleResponse ({
              speech: "Those are the materials available: " + materials.join(", "),
              text: "Those are the materials available:  \n- " + materials.join("  \n- "),
            }));
            return Promise.resolve(conv);
      })
      	.catch( err => {
            log.write(log.entry(METADATA, {message: err}));
            return Promise.resolve(conv);
        }); 
    })
      .catch( err => {
        log.write(log.entry(METADATA, {message: err}));
        return Promise.resolve(conv);
    }); 
  	//return Promise.resolve(conv);
	//return requestMaterialsSkore(conv, token);
});

exports.dialogflowFirebaseFulfillment = functions.https.onRequest(app);