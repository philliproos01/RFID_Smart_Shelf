using System;

// Reference the API

using ThingMagic;

// for Thread.Sleep

using System.Threading;

using System.Runtime.Remoting.Messaging;

 

internal class Program

{

    private static void Main(string[] args)

    {

        Reader r = null;

        r = Reader.Create("tmr:///COM7");

        //Uncomment this line to add default transport listener.

        //r.Transport += r.SimpleTransportListener;

        int[] antennaList = { 1,2 };

        r.Connect();

        while (true) {

            TagReadData[] tagReads;

        r.ParamSet("/reader/region/id", Reader.Region.NA);

        r.ParamSet("/reader/radio/readPower", 2000);

        // Create a simplereadplan which uses the antenna list created above

        SimpleReadPlan plan = new SimpleReadPlan(antennaList, TagProtocol.GEN2, null, null, 1000);

        // Set the created readplan

        r.ParamSet("/reader/read/plan", plan);

        // Read tags

        tagReads = r.Read(250);

       

            //Console.WriteLine("LOL");

 

            foreach (TagReadData tr in tagReads)

            {

                Console.WriteLine(tr.EpcString);

                int x = 1;

            }

        }

    }

}
