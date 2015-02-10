

displayView = function()
{
	// The code required to display a view.
	var tok = JSON.parse(localStorage.getItem("token"));
	var div = document.getElementById('nonlogview');
	var elem = document.getElementById('notlogview');
	if (tok != null){
		elem = document.getElementById('logview');
	}
	div.innerHTML = elem.innerHTML;
	if (tok != null){
		tabdisplay(1);
	}
};

window.onload = function()
{
	displayView();
};

function signup(){
	
	var pass1 = document.getElementById('password').value;
	var pass2 = document.getElementById('repeat_password').value;

	if (pass1 != pass2){
		window.alert('different passwords');
		return false;
	}

	if (pass1.length < 8){
		window.alert('password too short (min 8)');
		return false;
	}

	var dataform = {email: document.getElementById('email').value, password: document.getElementById('password').value, firstname: document.getElementById('firstname').value, familyname: document.getElementById('familyname').value, gender: document.getElementById('gender').value, city: document.getElementById('city').value, country: document.getElementById('country').value};

	var res = serverstub.signUp(dataform);

	window.alert(res.message);


};

function signin(json){
	var pass = document.getElementById('sipassword').value;

	if (pass.length < 8){
		window.alert('password too short (min 8)');
		return false;
	}

	var res = serverstub.signIn(document.getElementById('siemail').value, pass);
	var token = null;
	if (res.success == true){
	token = res.data;
	}
	localStorage.setItem("token", JSON.stringify(token));
	displayView();
	window.alert(res.message);
	return true;

};

function logout(){
	var tok = JSON.parse(localStorage.getItem("token"));
	localStorage.setItem("token", null);
	window.alert('youpi3');
	var res = serverstub.signOut(tok);

	displayView();
	return true;
};

function tabdisplay(id){

	switch(id){
		case 1 : 

			document.getElementById('browse').style.display ='none';
			document.getElementById('account').style.display ='none';
			var tok = JSON.parse(localStorage.getItem("token"));
			var res = serverstub.getUserDataByToken(tok);
			var usr = res.data;
			var usrinf = document.getElementById('userinfo');

			usrinf.innerHTML = "<div>Email : "+usr.email+"</div><b>Firstname : "+usr.firstname+"</b><div>Familyname : "+usr.familyname+"</div><div>Gender : "+usr.gender+"</div><div>City : "+usr.city+"</div><div>Country : "+usr.country+"</div>";
			
			reloadwall();

			document.getElementById('home').style.display='block';
			break;
		case 2 : 
			document.getElementById('home').style.display ='none';
			document.getElementById('account').style.display ='none';
			document.getElementById('browse').style.display='block';
			document.getElementById('showwall').style.display ='none';
			break;
		case 3 : 
			document.getElementById('browse').style.display ='none';
			document.getElementById('home').style.display ='none';
			document.getElementById('account').style.display='block';
			break;
		default:
			document.getElementById('browse').style.display ='none';
			document.getElementById('account').style.display ='none';
			document.getElementById('home').style.display='none';
			break;
	}

	return true;

};


function changepass()
{

	var tok = JSON.parse(localStorage.getItem("token"));
	var oldpass = document.getElementById('oldpwd').value;
	var newpass = document.getElementById('newpwd').value;

	if (newpass.length < 8){
		window.alert('password too short (min 8)');
		return false;
	}

	var res = serverstub.changePassword(tok, oldpass, newpass);

	window.alert(res.message);

};


function postmess(mail)
{
	var tok = JSON.parse(localStorage.getItem("token"));
	var content = document.getElementById('newmess').value;
	var res;
	if (mail) 
	{
		content = document.getElementById('newmessonwall').value;
		var email = JSON.parse(localStorage.getItem("usrmail"));
		res = serverstub.postMessage(tok, content, email);

	} else res = serverstub.postMessage(tok, content, null);

	window.alert(res.message);

};

function reloadwall(type)
{
	var tok = JSON.parse(localStorage.getItem("token"));
	var messages = serverstub.getUserMessagesByToken(tok).data;
	var wall = document.getElementById('wall');
	if (type) { 
		wall=document.getElementById('wallb');
		var email = JSON.parse(localStorage.getItem("usrmail"));
		messages = serverstub.getUserMessagesByEmail(tok, email).data; 

	}
		var wallcontent ="";
		for (var m=0; m<messages.length; m++)
		{
			wallcontent += "<div><h4>"+messages[m].writer+"</h4><p>"+messages[m].content+"</p></div></br>";
		};
		wall.innerHTML = wallcontent;
};


function finduser()
{

	var tok = JSON.parse(localStorage.getItem("token"));
	var mail = document.getElementById('usermail').value;

	document.getElementById('showwall').style.display ='block';

	var messages = serverstub.getUserMessagesByEmail(tok, mail).data;
	var wallb = document.getElementById('wallb');

	var res = serverstub.getUserDataByEmail(tok, mail);
			var usr = res.data;
			var usrinf = document.getElementById('userwallinfo');

			usrinf.innerHTML = "<div>Email : "+usr.email+"</div><b>Firstname : "+usr.firstname+"</b><div>Familyname : "+usr.familyname+"</div><div>Gender : "+usr.gender+"</div><div>City : "+usr.city+"</div><div>Country : "+usr.country+"</div>";
			

	var wallcontent ="";
		for (var m=0; m<messages.length; m++)
		{
			wallcontent += "<div><h4>"+messages[m].writer+"</h4><p>"+messages[m].content+"</p></div></br>";
		};
		wallb.innerHTML = wallcontent;
		localStorage.setItem("usrmail", JSON.stringify(mail));
		return false;
};


