# projectwalleyt

Well if you are reading this, you already know the **AWESOME** product we will be talking about.


# Welcome to the Future of Payment Gateway!!!
Knocking at the doors of 21st century, this is how we will end 1990s, by giving the world its first digital wallet system allowing customers to transfer money without visiting a Bank!!! YES, you read it first here, no need to go to Bank anymore.
With its 1st version out in the market, the software offers following features with many more fantastic features lined up for future releases.
A quick introduction to all the hype around:
- A new User can register i.e. just choose a *username* and *password* and as this is all about money, we need to record some sort of ID number which could be NRIC or passport #. 
- When a USER is created, we immediately create a new account with *status* as INACTIVE and return back his *Account Number* (a 10 digit random #). We could also retrieve Account Number using *get* user method.
- Once a *Account* is created for a new user, the status of the account is *INACTVE*. This status needs to be **changed to "ACTIVE"** before performing any actions. I have already set up an "staff" in employee table and with this staff login we can change it to *ACTIVE*
- User can now check balance after account is ACTIVE
- User can deposit some amount of money.
- User can check for his balance.
- User can transfer money to another account.
- User can check all his transactions.
- **IMP NOTE**: We are mimicking a deposit of money from bank or some external source and this is denoted by acc_num = 1000000. Also while running the app I am also setting up 3 users with their account # in the system. Username: user1, user2 and user3 with same password: *secure*

A quick tour of the *state of the art* API gateway this product offers.
## End Points
### "/user"
#### post  
##### Request: http://127.0.0.1:5000/user
			Body: {"name": "user4",
					  "pwd": "secure",
					  "id_num": "12345AAAA"}
			Res:  {"message": "User created",
				     "account_number": 3980316993,
				     "account_status": "INACTIVE"}

#### get
##### Request: http://127.0.0.1:5000/user
			Body: {"name": "user4",
				     "pwd": "secure"}
			Res:  {"account_number": 3980316993,
				     "account_status": "INACTIVE"}

### "/activate"
#### post
##### Request: http://127.0.0.1:5000/activate
As mentioned earlier, to active an account, a staff/employee needs to do it and I have already manually entered a record in EmployeeModel as "staff" and pwd as "secure". So to activate any user, please use below details with acc_num to be activated.

			Body: {"name": "staff",
				     "pwd": "secure",
				     "acc_num": 2736565246}
			Res:  {"message": "Account Activated"}

### "/deposit"
#### post
##### Request: http://127.0.0.1:5000/user
			Body: {"name": "user1",
				     "pwd": "secure",
				     "amount": 2000}
			Res:  {"message": "Deposit successful, new balance: 2000"}

### "/balance"  
#### get
##### Request: http://127.0.0.1:5000/user
			Body: {"name": "user1",
				     "pwd": "secure"}
			Res:  {"balance": 2000}

### "/transfer"
#### post
##### Request: http://127.0.0.1:5000/user
			Body: {"name": "user1",
				   "pwd": "secure",
				   "amount" :450,
				   "to_acc_num": 8975927435,
				   "message": "loan"}
			Res:  {"message":  "Transfer successful, new balance: 2350"}

### "/transactions"
#### get
##### Request: http://127.0.0.1:5000/user
			Body: {	"name": "user1",
					"pwd": "secure"}
			Res:  { "transactions": [
			        {
			            "from": "2736565246<user1>",
			            "to": "8975927435<user2>",
			            "amount": "-450.0",
			            "msg": "loan",
			            "date": "24/09/2020 00:04:54",
			            "interim_balance": 2350
			        },
			        {
			            "from": "Third party source",
			            "to": "2736565246<user1>",
			            "amount": "+800.0",
			            "msg": "Money deposited: External Source",
			            "date": "24/09/2020 00:03:08",
			            "interim_balance": 2800
			        },
			        {
			            "from": "Third party source",
			            "to": "2736565246<user1>",
			            "amount": "+2000.0",
			            "msg": "Money deposited: External Source",
			            "date": "24/09/2020 00:00:06",
			            "interim_balance": 2000
			        }
			    ],
			    "balance": 2350
			}
      
# To Run:
- docker build -t walleyt:latest .
- docker run -p 5000:5000 -i -t walleyt
- Then you can access the end points as mentioned above

# If we had more than 24hrs in a day we could:
- Use *Serializers/Marshmallow* for incoming and outgoing data
- Use *Blueprints/Namespace* to decouple all sub features
- Increased the test coverage
- Used JWT to tokenize the authentication process
- Use swagger to add all the swag around API documentation

### Would like to propose these features to increase the fan base of our product.
- Introduce referral programs and reward both the existing customer who referred and new customer with some rewards.
- Offer cashback or discounts to encourage our loyal customers to use us more and more
- Introduce multi-currency/cross border payment system
- Tie up with various banks and integrate their service so that a customer's accounts in various other banks consolidate under one umbrella and let him access all his account using our app/service
