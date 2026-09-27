import 'package:flutter/material.dart';

import '../../progress/screens/progress_screen.dart';
import '../../progress/screens/add_progress_screen.dart';
import '../../voice/screens/voice_notes_screen.dart';

import '../goal_model.dart';



class GoalCard extends StatelessWidget {


  final Goal goal;


  final VoidCallback? onEdit;


  final VoidCallback? onDelete;


  final bool isTherapist;



  const GoalCard({

    super.key,

    required this.goal,

    this.onEdit,

    this.onDelete,

    required this.isTherapist,

  });






  Color statusColor() {


    switch(goal.status.toUpperCase()) {


      case "COMPLETED":

        return Colors.green;



      case "ACTIVE":

        return Colors.blue;



      case "PENDING":

        return Colors.orange;



      default:

        return Colors.grey;

    }

  }









  Future<void> confirmDelete(
      BuildContext context) async {


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

            style:
                ElevatedButton.styleFrom(

              backgroundColor:
                  Colors.red,

              foregroundColor:
                  Colors.white,

            ),



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




    if(confirm == true) {

      onDelete?.call();

    }


  }









  @override
  Widget build(BuildContext context) {


    return Card(


      margin:
          const EdgeInsets.only(
            bottom: 16,
          ),


      elevation: 3,



      child: Padding(


        padding:
            const EdgeInsets.all(18),



        child: Column(


          crossAxisAlignment:
              CrossAxisAlignment.start,



          children: [





            Row(



              children: [




                Expanded(


                  child: Column(


                    crossAxisAlignment:
                        CrossAxisAlignment.start,


                    children: [



                      Text(


                        goal.shortTermGoal,


                        style:
                            const TextStyle(


                          fontSize: 20,


                          fontWeight:
                              FontWeight.bold,


                        ),


                      ),





                      const SizedBox(
                        height: 5,
                      ),





                      Text(

                        goal.domain,

                        style:
                            TextStyle(

                          color:
                              Colors.grey.shade600,

                        ),

                      ),


                    ],


                  ),


                ),





                if(isTherapist)


                  PopupMenuButton<String>(



                    onSelected:
                        (value) async {



                      if(value == "edit") {


                        onEdit?.call();


                      }



                      if(value == "delete") {


                        await confirmDelete(
                          context,
                        );


                      }



                    },



                    itemBuilder:
                        (_) => [



                      const PopupMenuItem(

                        value:
                            "edit",

                        child:
                            Text(
                          "Edit",
                        ),

                      ),





                      const PopupMenuItem(

                        value:
                            "delete",

                        child:
                            Text(
                          "Delete",
                        ),

                      ),


                    ],


                  ),



              ],


            ),








            const SizedBox(
              height: 12,
            ),






            Text(


              goal.longTermGoal,


              style:

                  TextStyle(

                color:
                    Colors.grey.shade700,

              ),


            ),









            const SizedBox(
              height: 15,
            ),









            Row(


              children: [


                const Icon(

                  Icons.school,

                  size: 18,

                ),





                const SizedBox(
                  width: 8,
                ),






                Expanded(

                  child:
                      Text(

                    "Current Level: ${goal.currentLevel}",

                  ),

                ),


              ],


            ),










            const SizedBox(
              height: 20,
            ),










            Wrap(


              spacing: 10,


              runSpacing: 10,



              children: [





                ElevatedButton.icon(



                  onPressed: () {



                    if(goal.id != null) {



                      Navigator.push(



                        context,



                        MaterialPageRoute(



                          builder: (_) =>


                              ProgressScreen(


                                goalId:
                                    goal.id!,


                                isTherapist:
                                    isTherapist,


                              ),


                        ),



                      );



                    }



                  },



                  icon:
                      const Icon(
                    Icons.show_chart,
                  ),



                  label:
                      const Text(
                    "Progress",
                  ),



                ),







                OutlinedButton.icon(



                  onPressed: () {



                    Navigator.push(



                      context,



                      MaterialPageRoute(



                        builder: (_) =>


                            VoiceNotesScreen(


                              childId:
                                  goal.childId,


                              isTherapist:
                                  isTherapist,


                            ),


                      ),



                    );



                  },



                  icon:
                      const Icon(
                    Icons.mic,
                  ),



                  label:
                      const Text(
                    "Voice",
                  ),



                ),







                if(isTherapist)



                  OutlinedButton.icon(



                    onPressed: () {



                      if(goal.id != null) {



                        Navigator.push(



                          context,



                          MaterialPageRoute(



                            builder: (_) =>


                                AddProgressScreen(


                                  goalId:
                                      goal.id!,


                                ),


                          ),



                        );


                      }



                    },



                    icon:
                        const Icon(
                      Icons.add,
                    ),



                    label:
                        const Text(
                      "Add",
                    ),



                  ),



              ],


            ),







            const SizedBox(
              height: 15,
            ),









            Row(



              mainAxisAlignment:
                  MainAxisAlignment.spaceBetween,



              children: [




                Text(



                  "${goal.durationDays} Days",



                  style:
                      const TextStyle(


                    fontWeight:
                        FontWeight.w500,


                  ),


                ),







                Chip(



                  label:
                      Text(
                    goal.status,
                  ),




                  backgroundColor:

                      statusColor()
                          .withValues(alpha: 0.15),




                  labelStyle:

                      TextStyle(

                    color:
                        statusColor(),


                    fontWeight:
                        FontWeight.bold,


                  ),



                ),




              ],


            ),




          ],


        ),


      ),


    );


  }


}