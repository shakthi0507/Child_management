import 'package:flutter/material.dart';

import '../progress_model.dart';
import '../services/progress_service.dart';



class AddProgressScreen extends StatefulWidget {


  final int goalId;


  const AddProgressScreen({

    super.key,

    required this.goalId,

  });



  @override
  State<AddProgressScreen> createState() =>
      _AddProgressScreenState();

}





class _AddProgressScreenState
    extends State<AddProgressScreen> {


  final _formKey =
      GlobalKey<FormState>();


  final successController =
      TextEditingController();


  final attemptController =
      TextEditingController();


  final textController =
      TextEditingController();



  final ProgressService _service =
      ProgressService();



  bool loading = false;
  bool milestonesLoading = true;
  List<Map<String, dynamic>> milestones = [];
  int? selectedMilestoneId;





  @override
  void dispose() {


    successController.dispose();

    attemptController.dispose();

    textController.dispose();


    super.dispose();

  }

  @override
  void initState() {
    super.initState();
    loadMilestones();
  }

  Future<void> loadMilestones() async {
    try {
      final result = await _service.getGoalMilestones(widget.goalId);
      if (!mounted) return;
      setState(() {
        milestones = result;
        selectedMilestoneId = result.isNotEmpty
            ? (result.first["id"] as num).toInt()
            : null;
        milestonesLoading = false;
      });
    } catch (error) {
      if (!mounted) return;
      setState(() => milestonesLoading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Unable to load milestones: $error")),
      );
    }
  }






  Future<void> saveProgress() async {


    if(!_formKey.currentState!.validate()) {

      return;

    }



    final successCount =
        int.parse(
          successController.text,
        );


    final attemptCount =
        int.parse(
          attemptController.text,
        );



    if(successCount > attemptCount){


      ScaffoldMessenger.of(context)
          .showSnackBar(

        const SnackBar(

          content:
              Text(
            "Success count cannot be greater than attempts",
          ),

        ),

      );


      return;

    }




    setState(() {

      loading = true;

    });





    if (selectedMilestoneId == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Select a milestone first")),
      );
      return;
    }

    try {



      final Progress progress = Progress(

        goalId: widget.goalId,

        milestoneId: selectedMilestoneId!,

        status: "IN_PROGRESS",

        notes:
            textController.text.trim(),

      );





      await _service.createProgress(
        progress,
      );





      if(!mounted) return;





      ScaffoldMessenger.of(context)
          .showSnackBar(


        const SnackBar(

          content:
              Text(
            "Progress added successfully",
          ),

          backgroundColor:
              Colors.green,

        ),


      );





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

            backgroundColor:
                Colors.red,

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







  Widget buildField({

    required TextEditingController controller,

    required String label,

    TextInputType type =
        TextInputType.text,

    int maxLines = 1,

  }) {


    return Padding(

      padding:
          const EdgeInsets.only(
            bottom: 18,
          ),



      child:
          TextFormField(


        controller:
            controller,


        keyboardType:
            type,


        maxLines:
            maxLines,



        validator: (value){


          if(value == null ||
              value.trim().isEmpty){


            return "$label is required";


          }



          if(type ==
              TextInputType.number){


            if(int.tryParse(value) == null){


              return "Enter valid number";


            }


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
          "Add Progress",
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

              if (milestonesLoading)
                const CircularProgressIndicator()
              else if (milestones.isEmpty)
                const Text("No milestones available for this goal")
              else
                DropdownButtonFormField<int>(
                  value: selectedMilestoneId,
                  decoration: const InputDecoration(
                    labelText: "Milestone",
                    border: OutlineInputBorder(),
                  ),
                  items: milestones.map((milestone) {
                    return DropdownMenuItem<int>(
                      value: (milestone["id"] as num).toInt(),
                      child: Text(milestone["title"]?.toString() ?? "Milestone"),
                    );
                  }).toList(),
                  onChanged: (value) {
                    setState(() => selectedMilestoneId = value);
                  },
                ),

              const SizedBox(height: 18),



              buildField(

                controller:
                    successController,

                label:
                    "Success Count",

                type:
                    TextInputType.number,

              ),





              buildField(

                controller:
                    attemptController,

                label:
                    "Attempt Count",

                type:
                    TextInputType.number,

              ),





              buildField(

                controller:
                    textController,

                label:
                    "Progress Notes",

                maxLines:
                    4,

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
                    ElevatedButton.icon(


                  onPressed:
                      loading
                          ? null
                          : saveProgress,



                  icon:
                      loading

                          ? const SizedBox(

                              width:
                                  18,

                              height:
                                  18,

                              child:
                                  CircularProgressIndicator(
                                strokeWidth:
                                    2,
                              ),

                            )


                          : const Icon(
                              Icons.save,
                            ),




                  label:
                      Text(

                    loading

                        ? "Saving..."

                        : "Save Progress",

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