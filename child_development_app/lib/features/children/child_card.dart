import 'package:flutter/material.dart';

import '../../shared/models/child_model.dart';
import 'child_details_screen.dart';


class ChildCard extends StatelessWidget {

  final ChildModel child;


  const ChildCard({
    super.key,
    required this.child,
  });



  @override
  Widget build(BuildContext context) {


    return Card(

      elevation: 3,

      margin:
          const EdgeInsets.symmetric(
            vertical: 8,
          ),


      child: InkWell(

        borderRadius:
            BorderRadius.circular(12),


        onTap: () {


          Navigator.push(

            context,

            MaterialPageRoute(

              builder: (_) =>

                  ChildDetailsScreen(

                    child: child,

                    // Parent does not have therapist id
                    therapistId: null,

                  ),

            ),

          );


        },


        child: ListTile(

          leading:
              const CircleAvatar(

            child:
                Icon(
              Icons.child_care,
            ),

          ),


          title:
              Text(
            child.name,
          ),


          subtitle:
              Text(

            "${child.gender}\n"
            "DOB: ${child.dob}\n"
            "${child.height} cm • ${child.weight} kg",

          ),


          isThreeLine:
              true,


          trailing:
              const Icon(
            Icons.arrow_forward_ios,
          ),


        ),

      ),

    );


  }

}