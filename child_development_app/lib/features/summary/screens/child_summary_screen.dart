import 'package:flutter/material.dart';

import '../models/child_summary_model.dart';

import '../services/summary_service.dart';



class ChildSummaryScreen extends StatefulWidget {


  final int childId;



  const ChildSummaryScreen({

    super.key,

    required this.childId,

  });



  @override
  State<ChildSummaryScreen> createState()
      => _ChildSummaryScreenState();

}





class _ChildSummaryScreenState
    extends State<ChildSummaryScreen> {



  final SummaryService service =
      SummaryService();



  ChildSummary? summary;


  bool loading = true;




  @override
  void initState(){

    super.initState();

    loadSummary();

  }







  Future<void> loadSummary() async {


    try {


      summary =
          await service.getSummary(
            widget.childId,
          );


    }
    catch(e){


      if(mounted){

        ScaffoldMessenger.of(context)
            .showSnackBar(

          SnackBar(
            content:
                Text(
              e.toString(),
            ),
          ),

        );

      }

    }



    if(mounted){

      setState(() {

        loading=false;

      });

    }


  }






  Color riskColor(String risk){


    switch(risk.toUpperCase()){


      case "LOW":

        return Colors.green;


      case "MEDIUM":

        return Colors.orange;


      case "HIGH":

        return Colors.red;


      default:

        return Colors.grey;

    }


  }








  @override
  Widget build(BuildContext context){


    return Scaffold(


      appBar:

          AppBar(

        title:
            const Text(
          "Child Summary",
        ),

      ),





      body:

          loading


          ?

          const Center(

            child:
                CircularProgressIndicator(),

          )



          :

          summary == null


          ?

          const Center(

            child:
                Text(
              "No summary found",
            ),

          )



          :

          ListView(


            padding:
                const EdgeInsets.all(20),



            children: [




              Card(

                child:
                    ListTile(

                  leading:
                      const Icon(
                    Icons.child_care,
                  ),

                  title:
                      Text(
                    summary!.child.name,
                  ),

                  subtitle:
                      Text(
                    "${summary!.child.gender}\nDOB: ${summary!.child.dob}",
                  ),

                ),

              ),




              const SizedBox(
                height:15,
              ),





              Card(

                child:
                    Padding(

                  padding:
                      const EdgeInsets.all(20),


                  child:
                      Column(

                    children: [


                      const Text(

                        "Goal Progress",

                        style:
                            TextStyle(

                          fontSize:18,

                          fontWeight:
                              FontWeight.bold,

                        ),

                      ),



                      const SizedBox(
                        height:10,
                      ),



                      Text(

                        "${summary!.successRate}%",

                        style:
                            const TextStyle(

                          fontSize:32,

                          fontWeight:
                              FontWeight.bold,

                        ),

                      ),


                    ],

                  ),

                ),

              ),






              Card(

                child:
                    ListTile(

                  leading:
                      Icon(

                    Icons.warning,

                    color:
                        riskColor(
                          summary!.riskLevel,
                        ),

                  ),

                  title:
                      const Text(
                    "Risk Level",
                  ),

                  subtitle:
                      Text(
                    summary!.riskLevel,
                  ),

                ),

              ),





              Card(

                child:
                    Padding(

                  padding:
                      const EdgeInsets.all(16),


                  child:
                      Text(
                    summary!.summary,
                  ),

                ),

              ),



            ],


          ),


    );

  }

}