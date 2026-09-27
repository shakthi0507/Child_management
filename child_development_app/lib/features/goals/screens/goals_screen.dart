import 'package:flutter/material.dart';

import '../../../core/api/api_service.dart';

import '../goal_model.dart';
import '../services/goal_service.dart';
import '../widgets/goal_card.dart';

import 'add_goal_screen.dart';
import 'edit_goal_screen.dart';



class GoalsScreen extends StatefulWidget {


  final int childId;

  final int? therapistId;

  final int? assessmentSessionId;



  const GoalsScreen({

    super.key,

    required this.childId,

    this.therapistId,

    this.assessmentSessionId,

  });



  @override
  State<GoalsScreen> createState() =>
      _GoalsScreenState();

}







class _GoalsScreenState
    extends State<GoalsScreen> {


  final GoalService _service =
      GoalService();



  List<Goal> goals = [];



  bool loading = true;



  String search = "";







  @override
  void initState() {

    super.initState();

    loadGoals();

  }








  Future<void> loadGoals() async {


    if(!mounted) return;



    setState(() {

      loading = true;

    });




    try {


      await ApiService.setToken();




      final result =
          await _service.getGoalsByChild(

            widget.childId,

          );




      if(!mounted) return;




      setState(() {

        goals = result;

      });



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









  Future<void> deleteGoal(
      int id
  ) async {


    final confirm =
        await showDialog<bool>(

      context: context,


      builder: (_) => AlertDialog(

        title:
            const Text(
          "Delete Goal",
        ),


        content:
            const Text(
          "Are you sure you want to delete this goal?",
        ),


        actions: [


          TextButton(

            onPressed: () {

              Navigator.pop(
                context,
                false,
              );

            },


            child:
                const Text(
              "Cancel",
            ),

          ),



          ElevatedButton(

            onPressed: () {

              Navigator.pop(
                context,
                true,
              );

            },


            child:
                const Text(
              "Delete",
            ),

          ),


        ],


      ),

    );





    if(confirm != true) return;





    final success =
        await _service.deleteGoal(id);




    if(success){


      await loadGoals();


    }
    else{


      if(mounted){

        ScaffoldMessenger.of(context)
            .showSnackBar(

          const SnackBar(

            content:
                Text(
              "Failed to delete goal",
            ),

          ),

        );

      }

    }


  }









  @override
  Widget build(BuildContext context) {


    final filtered =
        goals.where((goal){


      final text =
          search.toLowerCase();



      return goal.shortTermGoal
              .toLowerCase()
              .contains(text)

          ||

          goal.longTermGoal
              .toLowerCase()
              .contains(text);



    }).toList();







    return Scaffold(


      appBar:
          AppBar(

        title:
            const Text(
          "Goals",
        ),

      ),






      floatingActionButton:

          widget.therapistId != null

          ?

          FloatingActionButton.extended(


              icon:
                  const Icon(
                Icons.add,
              ),


              label:
                  const Text(
                "Add Goal",
              ),




              onPressed: () async {


                final created =
                    await Navigator.push(


                  context,


                  MaterialPageRoute(


                    builder: (_) =>

                        AddGoalScreen(


                      childId:
                          widget.childId,



                      therapistId:
                          widget.therapistId!,



                        assessmentSessionId:
                          widget.assessmentSessionId,


                    ),


                  ),


                );




                if(created == true){

                  await loadGoals();

                }



              },


            )

          : null,









      body:


          loading


          ?

          const Center(

            child:
                CircularProgressIndicator(),

          )



          :

          Column(


            children: [



              Padding(

                padding:
                    const EdgeInsets.all(
                  16,
                ),



                child:

                    TextField(


                  decoration:

                      InputDecoration(

                    hintText:
                        "Search Goal",


                    prefixIcon:
                        const Icon(
                      Icons.search,
                    ),



                    border:

                        OutlineInputBorder(

                      borderRadius:
                          BorderRadius.circular(
                        15,
                      ),

                    ),


                  ),



                  onChanged: (value){


                    setState(() {

                      search = value;

                    });


                  },


                ),


              ),





              Expanded(


                child:

                    RefreshIndicator(


                  onRefresh:
                      loadGoals,



                  child:


                      filtered.isEmpty


                      ?

                      ListView(

                        children: const [


                          SizedBox(
                            height:200,
                          ),



                          Center(

                            child:
                                Text(
                              "No Goals Found",
                            ),

                          ),


                        ],


                      )



                      :

                      ListView.builder(


                        padding:
                            const EdgeInsets.all(
                          16,
                        ),



                        itemCount:
                            filtered.length,



                        itemBuilder:
                            (_, index){



                          final goal =
                              filtered[index];




                          return GoalCard(


                            goal:
                                goal,



                            isTherapist:

                                widget.therapistId != null,




                            onEdit:


                                widget.therapistId != null

                                ?

                                () async {



                                  final result =

                                      await Navigator.push(


                                    context,


                                    MaterialPageRoute(


                                      builder: (_) =>

                                          EditGoalScreen(

                                        goal:
                                            goal,

                                      ),

                                    ),


                                  );




                                  if(result == true){

                                    await loadGoals();

                                  }



                                }


                                : null,





                            onDelete:


                                widget.therapistId != null

                                ?

                                () => deleteGoal(

                                  goal.id!,

                                )

                                :

                                null,



                          );


                        },


                      ),


                ),


              ),


            ],


          ),



    );

  }


}