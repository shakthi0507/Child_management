import 'package:flutter/material.dart';

import '../goal_model.dart';
import '../services/goal_service.dart';


class EditGoalScreen extends StatefulWidget {

  final Goal goal;


  const EditGoalScreen({
    super.key,
    required this.goal,
  });


  @override
  State<EditGoalScreen> createState() =>
      _EditGoalScreenState();

}



class _EditGoalScreenState
    extends State<EditGoalScreen> {


  final _formKey =
      GlobalKey<FormState>();


  late TextEditingController shortTermController;

  late TextEditingController longTermController;

  late TextEditingController durationController;


  final GoalService service =
      GoalService();


  bool loading = false;



  @override
  void initState() {

    super.initState();


    shortTermController =
        TextEditingController(
      text: widget.goal.shortTermGoal,
    );


    longTermController =
        TextEditingController(
      text: widget.goal.longTermGoal,
    );


    durationController =
        TextEditingController(
      text: widget.goal.durationDays.toString(),
    );

  }



  @override
  void dispose() {

    shortTermController.dispose();

    longTermController.dispose();

    durationController.dispose();

    super.dispose();

  }





  Future<void> updateGoal() async {


    if(!_formKey.currentState!.validate()){

      return;

    }


    setState(() {

      loading = true;

    });



    try {


      final success =
        await service.updateGoal(

      goalId:
          widget.goal.id!,


      shortTermGoal:
          shortTermController.text.trim(),


      longTermGoal:
          longTermController.text.trim(),


      durationDays:
          int.parse(
            durationController.text.trim(),
          ),


      status:
          widget.goal.status,

    );



      if(!success){

        throw Exception(
          "Failed to update goal",
        );

      }



      if(!mounted) return;



      Navigator.pop(
        context,
        true,
      );



    } catch(e){


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







  Widget field(
      TextEditingController controller,
      String label) {


    return Padding(

      padding:
          const EdgeInsets.only(
            bottom: 18,
          ),


      child:
          TextFormField(

        controller:
            controller,


        maxLines:
            3,


        validator: (value){


          if(value == null ||
              value.trim().isEmpty){


            return "$label is required";


          }


          return null;

        },


        decoration:
            InputDecoration(

          labelText:
              label,


          border:
              OutlineInputBorder(

            borderRadius:
                BorderRadius.circular(
                  15,
                ),

          ),

        ),

      ),

    );

  }






  @override
  Widget build(BuildContext context) {


    return Scaffold(


      appBar:
          AppBar(

        title:
            const Text(
          "Edit Goal",
        ),

      ),



      body:
          SingleChildScrollView(


        padding:
            const EdgeInsets.all(
              20,
            ),



        child:
            Form(


          key:
              _formKey,



          child:
              Column(


            children: [


              field(
                shortTermController,
                "Short Term Goal",
              ),



              field(
                longTermController,
                "Long Term Goal",
              ),



              field(
                durationController,
                "Duration Days",
              ),




              const SizedBox(
                height: 30,
              ),




              SizedBox(

                width:
                    double.infinity,


                height:
                    55,



                child:
                    ElevatedButton(


                  onPressed:
                      loading
                          ? null
                          : updateGoal,



                  child:

                      loading

                          ? const CircularProgressIndicator()

                          :

                      const Text(
                        "Update Goal",
                      ),


                ),

              ),


            ],

          ),

        ),

      ),

    );

  }

}