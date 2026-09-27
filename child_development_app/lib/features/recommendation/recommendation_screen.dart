import 'package:flutter/material.dart';

import 'models/recommendation_model.dart';
import 'services/recommendation_service.dart';



class RecommendationScreen extends StatefulWidget {


  final int childId;



  const RecommendationScreen({

    super.key,

    required this.childId,

  });



  @override
  State<RecommendationScreen> createState() =>
      _RecommendationScreenState();


}







class _RecommendationScreenState
    extends State<RecommendationScreen> {



  final RecommendationService service =
      RecommendationService();



  Recommendation? recommendation;



  bool loading = true;









  @override
  void initState() {

    super.initState();

    loadRecommendation();

  }









  Future<void> loadRecommendation() async {


    try {


      final result =

          await service.getRecommendation(

            widget.childId,

          );



      if(!mounted) return;



      setState(() {


        recommendation = result;


      });



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









  Widget summaryCard(){


    return Card(


      elevation: 3,


      child:

          Padding(


        padding:

            const EdgeInsets.all(20),



        child:

            Column(


          children: [



            const Icon(

              Icons.psychology,

              size:

                  45,

            ),





            const SizedBox(

              height: 10,

            ),





            const Text(


              "AI Analysis",



              style:

                  TextStyle(


                fontSize:

                    20,


                fontWeight:

                    FontWeight.bold,


              ),



            ),






            const SizedBox(

              height: 20,

            ),






            Text(



              "Active Goals: ${recommendation!.activeGoals}",



              style:

                  const TextStyle(


                fontSize:

                    22,


                fontWeight:

                    FontWeight.bold,


              ),



            ),



          ],


        ),


      ),


    );


  }









  Widget recommendationList(){



    if(recommendation!
        .recommendations
        .isEmpty){



      return const Card(


        child:

            Padding(


          padding:

              EdgeInsets.all(20),



          child:

              Text(


            "No AI recommendations available",

          ),



        ),


      );



    }







    return Column(



      crossAxisAlignment:

          CrossAxisAlignment.start,



      children: [




        const Text(



          "Recommendations",



          style:

              TextStyle(


            fontSize:

                20,


            fontWeight:

                FontWeight.bold,


          ),



        ),






        const SizedBox(

          height:

              10,

        ),







        ...recommendation!
            .recommendations
            .map(



          (item){



            return Card(



              margin:

                  const EdgeInsets.only(

                bottom:

                    10,

              ),




              child:

                  ListTile(



                leading:

                    const Icon(



                  Icons.check_circle,



                  color:

                      Colors.green,


                ),





                title:

                    Text(

                  item,

                ),



              ),



            );



          },


        ),



      ],


    );



  }









  @override
  Widget build(BuildContext context) {


    return Scaffold(



      appBar:

          AppBar(


        title:

            const Text(

          "AI Recommendation",

        ),



      ),







      body:


          loading



              ? const Center(


                  child:

                      CircularProgressIndicator(),


                )





              : recommendation == null



                  ? const Center(



                      child:

                          Text(


                        "No recommendation found",

                      ),


                    )





                  : RefreshIndicator(


                      onRefresh:

                          loadRecommendation,



                      child:

                          ListView(



                        padding:

                            const EdgeInsets.all(20),




                        children: [





                          summaryCard(),






                          const SizedBox(

                            height:

                                20,

                          ),





                          recommendationList(),




                        ],



                      ),


                    ),



    );


  }


}