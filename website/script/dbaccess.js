
// Initialize the Amazon Cognito credentials provider
AWS.config.region = 'us-west-2'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-west-2:b0efa991-65e7-4bcc-a02f-bca33a4e5676',
});

//global variable to hold data
var wegmans_tweets_detail_data=[];
var wegmans_tweets_words_data=[];


AWS.config.credentials.get(function(err) {
    if (err) {
        console.log("Error: "+err);
        return;
    }
    //console.log("Cognito Identity Id: " + AWS.config.credentials.identityId);
    var cognitoSyncClient = new AWS.CognitoSync();
    cognitoSyncClient.listDatasets({
        IdentityId: AWS.config.credentials.identityId,
        IdentityPoolId: "us-west-2:b0efa991-65e7-4bcc-a02f-bca33a4e5676"
    }, function(err, data) {
        if ( !err ) {
            //console.log(JSON.stringify(data));

//you can now check that you can describe the DynamoDB table
var params = {TableName: 'wegmans_tweets_detail' };
var dynamodb = new AWS.DynamoDB({apiVersion: '2012-08-10'});

//describe table
/*
dynamodb.describeTable(params, function(err, data){
    console.log(JSON.stringify(data));
})
*/

//get data from table
dynamodb.scan(params, function (err, data)
{

    wegmans_tweets_detail_data = data['Items'];

    $.getScript( "script/scatter.js", function() {
      console.log("scatter.js loaded"); // Data returned
    });

    $.getScript( "script/mapping.js", function() {
      console.log("mapping.js loaded"); // Data returned
    });

});

//scan word table
var params = {TableName: 'wegmans_tweets_words'};
dynamodb.scan(params, function (err, data)
{
    wegmans_tweets_words_data = data['Items'];

    $.getScript( "script/bubble.js", function() {
      console.log("bubble.js loaded"); // Data returned
    });

});

}});

});
