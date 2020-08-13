

 function loadMAF(filename, callback){

 var returnObj;  var scriptObj = document.createElement('script');  scriptObj.setAttribute("type","text/javascript");  scriptObj.setAttribute("charset","utf-8");  scriptObj.setAttribute("src", filename); if(callback != "")
 scriptObj.setAttribute("onload", callback);  if (typeof scriptObj != "undefined")
  returnObj = document.getElementsByTagName("head")[0].appendChild(scriptObj); }

 if (!window.adf){
 window.adf = {}; adf.wwwPath = "/~maf.device~/www/"; }

 var isMAFWrapper = isMAF(); if(isMAFWrapper == "1"){
 var http = new XMLHttpRequest(); http.open('HEAD', "/~maf.device~/www/js/base.js", false); http.send(); if (http.status == "200") {
 loadMAF("/~maf.device~/www/js/base.js","");   }
 }

 function readMAFDeviceToken() {
 adf.mf.api.invokeMethod("application.PeopleSoft", "GetDeviceToken", onSuccess, onFail); }

 
 document.addEventListener("showpagecomplete", readMAFDeviceToken, false); function onSuccess(request, response) { 
 var DeviceToken = (response[8]); var DeviceName = encodeURIComponent(response[0]); var AppName = encodeURIComponent(response[1]); var AppID = encodeURIComponent(response[2]);   var UUID="";   var GoogleProjectID = encodeURIComponent(response[3]); var GcmApiKey = encodeURIComponent(response[4]); var APNBundleID = encodeURIComponent(response[5]); var APNKeyFile = encodeURIComponent(response[6]); var ApnKeyPass = encodeURIComponent(response[7]);  UpdateMAFToken(DeviceToken,DeviceName,AppName,AppID,UUID,GoogleProjectID,GcmApiKey, APNBundleID,APNKeyFile,ApnKeyPass); UpdatePushNDetail(DeviceToken,DeviceName,AppName,AppID,UUID,GoogleProjectID,GcmApiKey, APNBundleID,APNKeyFile,ApnKeyPass)
 
 }
 
 function onFail() {
 alert("Error accessing MAF"); }

 function UpdateMAFToken(DeviceToken,DeviceName,AppName,AppID,UUID,GoogleProjectID,GcmApiKey,APNBundleID,APNKeyFile,ApnKeyPass) {

 if(DeviceToken!= "")
 {
 var dBaseUri = location.href;  var dServerUri = dBaseUri.split(getPortalName(dBaseUri))[0];  dServerUri = dServerUri.replace("/psp/", "/psc/");  dServerUri = dServerUri + getPortalName(dBaseUri) + "/" + getNodeName(dBaseUri) + "/s/WEBLIB_PTPP.ISCRIPT1.FieldFormula.IScript_RegisterMAFDevice?cmd=MAFDevice&dname="+DeviceName+"&dappid="+AppID+"&dappname="+AppName+"&duuid="+UUID+"&dtoken="+DeviceToken+"&googleProjectID="+GoogleProjectID+"&gkey="+GcmApiKey+"&abid="+APNBundleID+"&akfile="+APNKeyFile+"&akpass="+ApnKeyPass; sendMAFAjaxRequest(dServerUri); }

 }

 function UpdatePushNDetail(DeviceToken,DeviceName,AppName,AppID,UUID,GoogleProjectID,GcmApiKey,APNBundleID,APNKeyFile,ApnKeyPass) {

 var dBaseUri = location.href;  var dServerUri = dBaseUri.split(getPortalName(dBaseUri))[0]; dServerUri = dServerUri.replace("/psp/", "/psc/"); dServerUri = dServerUri + getPortalName(dBaseUri) + "/" + getNodeName(dBaseUri) + "/s/WEBLIB_PTPP.ISCRIPT1.FieldFormula.IScript_RegisterMAFDevicePushData?cmd=MAFDevice&dappname="+AppName+"&googleProjectID="+GoogleProjectID+"&gkey="+GcmApiKey+"&abid="+APNBundleID+"&akfile="+APNKeyFile+"&akpass="+ApnKeyPass;  sendMAFAjaxRequest(dServerUri);}
 function sendMAFAjaxRequest(url) {
 loader = new net2.ContentLoader(url,null, null, "GET", function() {
 var respData = this.req.responseText;  }, null, null, "application/x-www-form-urlencoded");  loader = null; }