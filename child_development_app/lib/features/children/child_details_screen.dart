import 'package:flutter/material.dart';

import '../../shared/models/child_model.dart';

import '../assessment/screens/assessment_screen.dart';
import '../goals/screens/goals_screen.dart';
import '../recommendation/screens/recommendation_screen.dart';
import '../voice/screens/voice_notes_screen.dart';

import 'edit_child_screen.dart';
import '../summary/screens/child_summary_screen.dart';
import '../summary/services/summary_service.dart';
import '../summary/models/child_summary_model.dart';



class ChildDetailsScreen extends StatefulWidget {


  final ChildModel child;

  final int? therapistId;



  const ChildDetailsScreen({

    super.key,

    required this.child,

    this.therapistId,

  });



  @override
  State<ChildDetailsScreen> createState() =>
      _ChildDetailsScreenState();

}







class _ChildDetailsScreenState
    extends State<ChildDetailsScreen>
    with SingleTickerProviderStateMixin {



  late ChildModel child;


  late TabController _tabController;

  final SummaryService summaryService = SummaryService();

  ChildSummary? childSummary;

  bool summaryLoading = true;





  bool get isTherapist =>
      widget.therapistId != null;







  @override
  void initState() {

    super.initState();


    child = widget.child;


    loadChildSummary();

    _tabController =
        TabController(

      length: 4,

      vsync: this,

    );

  }







  @override
  void dispose() {

    _tabController.dispose();

    super.dispose();

  }









  Future<void> loadChildSummary() async {

    try {

      final result =
          await summaryService.getSummary(child.id);

      if(!mounted) return;

      setState(() {

        childSummary = result;

        summaryLoading = false;

      });

    } catch(e) {

      debugPrint(e.toString());

      if(mounted){

        setState(() {

          summaryLoading = false;

        });

      }

    }

  }


  Future<void> _editChild() async {


    final updatedChild =
        await Navigator.push<ChildModel>(

      context,

      MaterialPageRoute(

        builder: (_) =>
            EditChildScreen(

          child: child,

        ),

      ),

    );




    if(updatedChild != null){


      setState(() {

        child = updatedChild;

      });


    }


  }








  Future<void> _deleteChild() async {


    ScaffoldMessenger.of(context)
        .showSnackBar(

      const SnackBar(

        content:
            Text(
          "Delete API integration pending",
        ),

      ),

    );


  }









  Widget infoRow(

      IconData icon,

      String title,

      String value,

  ){


    return Padding(

      padding:
          const EdgeInsets.only(
            bottom: 14,
          ),


      child: Row(

        children: [


          Icon(icon),


          const SizedBox(
            width: 12,
          ),



          Expanded(

            child: Text(

              title,

              style:
                  const TextStyle(

                color:
                    Colors.grey,

              ),

            ),

          ),




          Text(

            value,

            style:
                const TextStyle(

              fontWeight:
                  FontWeight.bold,

            ),

          ),


        ],

      ),

    );

  }









  Widget summaryCard(

      IconData icon,

      String title,

      String value,

      Color color,

  ){


    return Expanded(


      child: Card(


        child: Padding(


          padding:
              const EdgeInsets.all(
                16,
              ),



          child: Column(


            children: [


              Icon(

                icon,

                size:
                    32,

                color:
                    color,

              ),



              const SizedBox(
                height: 10,
              ),



              Text(

                value,

                style:
                    const TextStyle(

                  fontSize:
                      22,

                  fontWeight:
                      FontWeight.bold,

                ),

              ),




              Text(title),


            ],


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
          "Child Details",
        ),




        actions: [



          if(isTherapist)

            IconButton(

              icon:
                  const Icon(
                Icons.edit,
              ),

              onPressed:
                  _editChild,

            ),





          if(isTherapist)

            IconButton(

              icon:
                  const Icon(
                Icons.delete,
              ),

              onPressed:
                  _deleteChild,

            ),



        ],



      ),







      body:


      ListView(


        padding:
            const EdgeInsets.all(
              16,
            ),



        children: [







          Card(


            child:
                Padding(


              padding:
                  const EdgeInsets.all(
                    20,
                  ),




              child: Column(


                children: [



                  const CircleAvatar(


                    radius:
                        50,


                    child:
                        Icon(

                      Icons.child_care,

                      size:
                          55,

                    ),


                  ),





                  const SizedBox(
                    height: 15,
                  ),





                  Text(


                    child.name,


                    style:
                        const TextStyle(

                      fontSize:
                          24,

                      fontWeight:
                          FontWeight.bold,

                    ),


                  ),




                  Text(
                    child.gender,
                  ),



                ],


              ),


            ),


          ),









          const SizedBox(
            height: 20,
          ),






          Row(


            children: [



              summaryCard(

                Icons.flag,

                "Goals",

                summaryLoading
                    ? "-"
                    : childSummary?.totalGoals.toString() ?? "0",

                Colors.blue,

              ),




              const SizedBox(
                width: 12,
              ),





              summaryCard(

                Icons.assignment,

                "Assessment",

                summaryLoading
                    ? "-"
                    : childSummary?.riskLevel ?? "N/A",

                Colors.orange,

              ),



            ],


          ),







          const SizedBox(
            height: 20,
          ),








          Card(


            child:
                Padding(


              padding:
                  const EdgeInsets.all(
                    16,
                  ),



              child: Column(


                children: [



                  infoRow(

                    Icons.person,

                    "Name",

                    child.name,

                  ),




                  infoRow(

                    Icons.wc,

                    "Gender",

                    child.gender,

                  ),





                  infoRow(

                    Icons.calendar_today,

                    "DOB",

                    child.dob,

                  ),





                  infoRow(

                    Icons.height,

                    "Height",

                    "${child.height} cm",

                  ),





                  infoRow(

                    Icons.monitor_weight,

                    "Weight",

                    "${child.weight} kg",

                  ),




                ],


              ),


            ),


          ),









          const SizedBox(
            height: 20,
          ),







          ElevatedButton.icon(


            onPressed: (){


              Navigator.push(


                context,


                MaterialPageRoute(


                  builder: (_) =>

                      ChildSummaryScreen(

                    childId:
                        child.id,

                  ),


                ),


              );


            },



            icon:
                const Icon(
              Icons.analytics,
            ),



            label:
                const Text(
              "View Summary",
            ),


          ),







          const SizedBox(
            height: 20,
          ),







          TabBar(


            controller:
                _tabController,



            tabs: const [



              Tab(

                icon:
                    Icon(
                  Icons.flag,
                ),

                text:
                    "Goals",

              ),




              Tab(

                icon:
                    Icon(
                  Icons.assignment,
                ),

                text:
                    "Assessment",

              ),





              Tab(

                icon:
                    Icon(
                  Icons.mic,
                ),

                text:
                    "Voice",

              ),





              Tab(

                icon:
                    Icon(
                  Icons.psychology,
                ),

                text:
                    "AI",

              ),



            ],



          ),







          SizedBox(


            height:
                500,



            child:


                TabBarView(


              controller:
                  _tabController,



              children: [




                GoalsScreen(

                  childId:
                      child.id,

                  therapistId:
                      widget.therapistId,

                ),





                AssessmentScreen(

                  childId:
                      child.id,

                  isTherapist:
                      isTherapist,

                ),





                VoiceNotesScreen(

                  childId:
                      child.id,

                  isTherapist:
                      isTherapist,

                ),





                RecommendationScreen(

                  childId:
                      child.id,

                ),




              ],


            ),


          ),





        ],


      ),



    );


  }


}