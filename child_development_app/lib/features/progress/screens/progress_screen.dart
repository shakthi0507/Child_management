import 'package:flutter/material.dart';

import '../progress_model.dart';
import '../services/progress_service.dart';
import 'add_progress_screen.dart';



class ProgressScreen extends StatefulWidget {


  final int goalId;


  final bool isTherapist;



  const ProgressScreen({

    super.key,

    required this.goalId,

    required this.isTherapist,

  });



  @override
  State<ProgressScreen> createState() =>
      _ProgressScreenState();

}






class _ProgressScreenState
    extends State<ProgressScreen> {



  final ProgressService _service =
      ProgressService();



  List<Progress> progressList = [];



  bool loading = true;





  @override
  void initState() {

    super.initState();

    loadProgress();

  }





  Future<void> loadProgress() async {


    if(!mounted) return;



    setState(() {

      loading = true;

    });




    try {


      progressList =
          await _service.getGoalProgress(
            widget.goalId,
          );



    } catch(e) {


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

        loading = false;

      });

    }


  }






  double get overallProgress {

  if(progressList.isEmpty){
    return 0;
  }


  int completed = progressList
      .where(
        (p) => p.status.toUpperCase() == "COMPLETED",
      )
      .length;


  return completed / progressList.length;

}







  Future<void> openAddProgress() async {


    final result =
        await Navigator.push(


      context,


      MaterialPageRoute(


        builder: (_) =>

            AddProgressScreen(

          goalId:
              widget.goalId,

        ),


      ),


    );




    if(result == true){

      loadProgress();

    }


  }







  @override
  Widget build(BuildContext context) {



    return Scaffold(



      appBar: AppBar(


        title:
            const Text(
          "Progress",
        ),


      ),





      floatingActionButton:


          widget.isTherapist


          ? FloatingActionButton.extended(


              onPressed:
                  openAddProgress,



              icon:
                  const Icon(
                Icons.add,
              ),



              label:
                  const Text(
                "Add Progress",
              ),


            )


          : null,







      body:


          loading


          ? const Center(

              child:
                  CircularProgressIndicator(),

            )



          : RefreshIndicator(


              onRefresh:
                  loadProgress,



              child: ListView(


                padding:
                    const EdgeInsets.all(
                      16,
                    ),



                children: [






                  Card(



                    elevation: 3,



                    child: Padding(



                      padding:
                          const EdgeInsets.all(
                            20,
                          ),




                      child: Column(



                        children: [



                          const Text(

                            "Overall Progress",

                            style:
                                TextStyle(

                              fontSize:
                                  18,

                              fontWeight:
                                  FontWeight.bold,

                            ),

                          ),





                          const SizedBox(
                            height: 20,
                          ),





                          CircularProgressIndicator(


                            value:
                                overallProgress,


                            strokeWidth:
                                10,


                          ),






                          const SizedBox(
                            height: 15,
                          ),





                          Text(


                            "${(overallProgress * 100).toStringAsFixed(1)}%",


                            style:
                                const TextStyle(

                              fontSize:
                                  24,

                              fontWeight:
                                  FontWeight.bold,

                            ),


                          ),



                        ],


                      ),


                    ),


                  ),






                  const SizedBox(
                    height: 20,
                  ),







                  if(progressList.isEmpty)


                    const Padding(


                      padding:
                          EdgeInsets.all(
                            40,
                          ),



                      child:
                          Center(

                        child:
                            Text(
                          "No progress records found",
                        ),

                      ),



                    )



                  else



                    ...progressList.map(


                      (progress){


                        return Card(


                          margin:
                              const EdgeInsets.only(
                            bottom: 12,
                          ),




                          child:
                              ListTile(



                            leading:
                              CircleAvatar(
                                child:
                                    Icon(
                                  progress.status.toUpperCase() == "COMPLETED"
                                      ? Icons.check_circle
                                      : progress.status.toUpperCase() == "IN_PROGRESS"
                                          ? Icons.timelapse
                                          : Icons.pending,
                                ),
                              ),


                          title:
                              Text(
                                progress.notes ?? "No notes",
                              ),


                          subtitle:
                              Text(
                                progress.status,
                              ),


                          trailing:
                              Chip(
                                label:
                                    Text(
                                      progress.status,
                                    ),
                              ),


                            ),



                          );

                      },

                    ),



                ],


              ),


            ),



    );

  }


}