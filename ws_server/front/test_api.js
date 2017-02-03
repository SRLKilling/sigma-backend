WS = new SigmaWS("ws://localhost:80/ws");

function sendAuth() {
	token = document.getElementById("token").value;
	transaction = new AuthenticationTransaction(WS, token);
	transaction.onmessage = function(resp) {
		if(resp.code == 0) document.getElementById("authresp").innerHTML = "Successfully identified";
		else if(resp.code == 112) document.getElementById("authresp").innerHTML = "Identification error";
	}
	transaction.sendOriginalMessage();
}

function Ressource(fields) {
	this.fields = [];
	
	this.add_field = function(p_type, p_name, p_apiname, p_def) {
		var obj = {type: p_type, name: p_name, apiname: p_apiname, def: p_def};
		this.fields.push(obj);
	};
	
	this.create_form = function() {
		this.form_node = document.createElement("form");
		this.inputs = {};
		for(i in this.fields) {
			f = this.fields[i];
			label = document.createElement("label");
			label.appendChild( document.createTextNode(f.name + " : ") );
			label.for = f.apiname;
			
			input = document.createElement("input");
			input.type = f.type;
			input.name = f.apiname;
			input.id = f.apiname;
			input.value = f.def;
			this.inputs[f.apiname] = input;
			
			this.form_node.appendChild(label);
			this.form_node.appendChild(input);
			this.form_node.appendChild(document.createElement("br"));
		};
	};
	
	this.display = function() {
		d = document.getElementById("form_container");
		if(d.firstChild != null)
			d.removeChild( d.firstChild );
		d.appendChild( this.form_node );
	}
	
	this.content = function() {
		obj = {}
		for(n in this.inputs) {
			input = this.inputs[n];
			if(input.value != "")
				obj[n] = input.value;
		}
		return obj;
	}
	
	return this;
}

function RessourceList() {
	this.ressources = {}
	
	this.add = function(name, obj) {
		r = new Ressource();
		for(i in obj) {
			f = obj[i];
			r.add_field(f[0], f[1], f[2], f[3]);
		}
		this.ressources[name] = r;
	};
	
	this.generate_DOM = function() {
		list = document.createElement("ul");
		for(n in this.ressources) {
			r = this.ressources[n];
			
			r.create_form();
			li = document.createElement("li");
			a = document.createElement("a");
			a.appendChild( document.createTextNode(n) );
			a.href = "#";
			a.onclick = (function(obj) {
				return function() {
					obj.change_form(n);
				};
			})(this)
			li.appendChild(a);
			list.appendChild(li);
		}
		
		document.getElementById("form_chooser").appendChild(list);
	};
	
	this.change_form = function(n) {
		this.ressources[n].display();
		this.currentRes = this.ressources[n];
	};
	
	return this;
}

ressources = new RessourceList();

function send() {
	loc = document.getElementById("action_location").value;
	action = document.getElementById("action_name").value;
	data = ressources.currentRes.content();
	pk = document.getElementById("action_pk").value;
	if(pk == "") pk = null;
	
	transaction = new RESTTransaction(WS, loc, action, data, pk);
	transaction.onmessage = function(resp) {
		document.getElementById("response").innerHTML = "<pre>" + JSON.stringify(resp,null,2) + "</pre>";
	}
	transaction.s = performance.now();
	transaction.sendOriginalMessage();
}

function onload() {
	ressources.generate_DOM();
}