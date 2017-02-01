function SigmaWS(url) {
	this.ws = new WebSocket(url);
	this.transactions = {}
	this.nextTransactionId = 0
	
	this.registerTransaction = function(transaction) {
		id = this.nextTransactionId;
		this.nextTransactionId += 1;
		
		transaction.id = id;
		this.transactions[id] = transaction
	}
	
	this.send = function(msg) {
		msg = JSON.stringify(msg)
		this.ws.send(msg);
	}
	
	this.ws.onmessage = (function(self){
			return function(msg_event){
				msg = JSON.parse(msg_event.data);
			
				if(! 'id' in msg) { return; }
				if(msg.id < 0) { self.onevent(msg); return; }
				if(! msg.id in self.transactions) { return; }
				
				transaction = self.transactions[msg.id];
				transaction.onmessage(msg);
			}
		})(this);
	
	this.onevent = function(msg) {}
	
	return this;
}


function AuthenticationTransaction(ws, token) {
	this.ws = ws;
	this.ws.registerTransaction(this);
	
	this.sendOriginalMessage = function() {
		message = {
			id: this.id,
			protocol: "SIGMA.0.1",
			action: "AUTH",
			token: token
		}
		this.ws.send(message);
	}
	
	return this;
}

function RESTTransaction(ws, loc, action) {
	this.ws = ws;
	this.ws.registerTransaction(this);
	
	this.sendOriginalMessage = function() {
		message = {
			id : this.id,
			protocol: "SIGMA.0.1",
			action: "REST_API",
			REST_action: "",
			REST_location: "test",
		}
		this.ws.send(message);
	}
	
	return this;
}