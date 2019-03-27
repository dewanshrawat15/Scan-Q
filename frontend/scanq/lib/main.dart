import 'package:flutter/material.dart';
import 'dart:async';
import 'dart:convert';
import 'package:barcode_scan/barcode_scan.dart';
import 'package:flutter/services.dart';
import 'dart:io';
import 'package:http/http.dart' as http;

void main() => runApp(MyApp());

class AccountInfo{
  String username;
  String fullname;
  String email;

  AccountInfo({this.username, this.fullname, this.email});
}


// QR App Screen Here

class QRApp extends StatefulWidget {
  final AccountInfo accountUsername;
  QRApp({Key key, @required this.accountUsername});

  @override
  QRAppState createState() {
    return new QRAppState(qrappdata: accountUsername);
  }
}

class QRAppState extends State<QRApp> {
  final AccountInfo qrappdata;
  QRAppState({Key key, @required this.qrappdata});

  String result = "";

  Future _scanQR() async {
    try {
      String qrResult = await BarcodeScanner.scan();
      Map data = {
        'username': '${qrappdata.username}'
      };
      var jsonData = json.encode(data);
      http.post(qrResult, body: jsonData)
          .then((response){
        var t = response.body;
        Navigator.push(context, MaterialPageRoute(builder: (BuildContext context) => tickDisplay()));
      });
    } on PlatformException catch (ex) {
      if (ex.code == BarcodeScanner.CameraAccessDenied) {
        setState(() {
          result = "Camera permission was denied";
        });
      } else {
        setState(() {
          result = "Unknown Error $ex";
        });
      }
    } on FormatException {
      setState(() {
        result = "You pressed the back button before scanning anything";
      });
    } catch (ex) {
      setState(() {
        result = "Unknown Error $ex";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Text(
          result,
          style: new TextStyle(fontSize: 30.0, fontWeight: FontWeight.bold),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        icon: Icon(Icons.camera_alt),
        label: Text("Scan"),
        onPressed: _scanQR,
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }
}

// QR Code Scanner Ends Here


// Home Screen Starts Here

class Home extends StatefulWidget {

  final AccountInfo data;

  Home({Key key, @required this.data}) : super(key: key);

  @override
  HomeState createState() => new HomeState(info: data,);
}

class AccountDet extends StatelessWidget{

  final AccountInfo accountInfo;
  AccountDet(
      {Key key, @required this.accountInfo}
      );


  @override
  Widget build(BuildContext context){
    // return Text("${accountInfo.fullname}");
    return Scaffold(
      body: Center(
        child: Column(
          // crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: <Widget>[
            Hero(
              tag: 'hero',
              child: Padding(
                padding: EdgeInsets.all(12.0),
                child: CircleAvatar(
                  radius: 72.0,
                  backgroundColor: Colors.black,
                  child: Text('${accountInfo.fullname[0].toUpperCase()}', style: TextStyle(fontSize: 36, color: Colors.white)),
                ),
              ),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text(
                '${accountInfo.username}',
                style: TextStyle(fontSize: 20.0, color: Colors.black),
              ),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text(
                '${accountInfo.fullname}',
                style: TextStyle(fontSize: 20.0, color: Colors.black),
              ),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text(
                '${accountInfo.email}',
                style: TextStyle(fontSize: 16.0, color: Colors.black),
              ),
            ),
          ],
        ),
      ),
    );
  }

}

class HomeState extends State<Home> with SingleTickerProviderStateMixin {
  TabController controller;

  final AccountInfo info;
  HomeState({Key key, @required this.info});

  @override
  void initState() {
    super.initState();
    controller = new TabController(length: 3, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return new Scaffold(
      appBar: new AppBar(
        title: Text('Scan-Q'),
        backgroundColor: Colors.black87,
      ),
      body: new TabBarView(
        children: <Widget>[
          AccountDet(accountInfo: info,),
          QRApp(accountUsername: info,),
          new Tab(icon: new Icon(Icons.list)),
        ],
        controller: controller,
      ),
      bottomNavigationBar: new Material(
        color: Colors.black87,
        child: new TabBar(
          indicatorColor: Colors.white,
          tabs: <Tab>[
            new Tab(
              icon: new Icon(Icons.account_circle, color: Colors.white),
            ),
            new Tab(
              icon: new Icon(Icons.camera_alt, color: Colors.white),
            ),
            new Tab(
              icon: new Icon(Icons.list, color: Colors.white),
            )
          ],
          controller: controller,
        ),
      ),
    );
  }
}

// Home Screen Ends Here


class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        primaryColor: Colors.black,
      ),
      debugShowCheckedModeBanner: false,
      home: MyCustomForm(),
    );
  }
}

class MyCustomForm extends StatefulWidget {
  @override
  _MyCustomFormState createState() => _MyCustomFormState();
}

class _MyCustomFormState extends State<MyCustomForm> {
  final myUsername = TextEditingController();
  final myPassword = TextEditingController();
  @override
  void dispose() {
    myUsername.dispose();
    myPassword.dispose();
    super.dispose();
  }

  void _showDialog() {
    // flutter defined function
    showDialog(
      context: context,
      builder: (BuildContext context) {
        // return object of type Dialog
        return AlertDialog(
          title: new Text("Wrong Credentials"),
          content: new Text("Wrong credentials entered. Try Again! "),
          actions: <Widget>[
            // usually buttons at the bottom of the dialog
            new FlatButton(
              child: new Text("Close"),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
  }

  apiRequest(String url, Map jsonMap) async{
    var temp = json.encode(jsonMap);
    http.post(url, body: temp)
        .then((response){
      var t = response.body;
      var jsonResult = json.decode(t.toString());
      var result = jsonResult["boolean"];
      if(result == true){
        myUsername.clear();
        myPassword.clear();
        var jsonusername = jsonResult["username"];
        var jsonname = jsonResult["name"];
        var jsonemail = jsonResult["email"];
        final data = AccountInfo(username: jsonusername, fullname: jsonname, email: jsonemail);
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => Home(data: data,)),
        );
      }
      else{
        _showDialog();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
          child: ListView(
            padding: EdgeInsets.symmetric(horizontal: 24.0),
            children: <Widget>[
              SizedBox(height: 80.0),
              Column(
                children: <Widget>[
                  SizedBox(height: 20.0),
                  Text('Login', style: TextStyle(fontSize: 24.0),),
                ],
              ),
              SizedBox(height: 120.0),
              TextField(
                decoration: InputDecoration(
                  labelText: 'Username',
                ),
                controller: myUsername,
              ),
              SizedBox(height: 12.0),
              TextField(
                decoration: InputDecoration(
                  labelText: 'Password',
                ),
                controller: myPassword,
                obscureText: true,
              ),
              ButtonBar(
                children: <Widget>[
                  RaisedButton(
                    child: Text('Login'),
                    onPressed: () {
                      String url = 'http://scanq.herokuapp.com/api/login/';
                      Map map = {
                        'username': myUsername.text,
                        'password': myPassword.text
                      };
                      apiRequest(url, map);
                    },
                  ),
                ],
              ),
            ],
          )
      ),
    );
  }
}


// ignore: camel_case_types
class tickDisplay extends StatelessWidget {
  final imag= new Image(image: new AssetImage("assets/tick.gif"));
  final text = new Text("Attendance recorded successfully");
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: new Text('Scan-Q'),
      ),
      body: Center(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            imag, text
          ],
        ),
      ),
    );


  }
}