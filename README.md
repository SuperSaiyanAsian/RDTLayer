# RDTLayer
An RDT (Reliable Data Transmission) layer implementation that allows the transfer of string data through an unreliable channel in a simulated environment.

<div align="justify">
For this project, I have used Python to implement a RDTLayer that runs successfully with the original, provided UnreliableChannel and Segment classes. It is able to deliver all of the data with no errors, succeeding even with all of the unreliable features enabled. There are at most 4 packets sent in one pipeline and a flow-control window is used to ensure that a maximum of 4 characters can be sent in one packet and that a maximum of 15 characters of data is sent in one iteration. Through cached sequence numbers, it also utilizes cumulative ack to update the next acknowledgement number accordingly. With segment timeouts through a count of iterations, packets that have time out are selectively retransmitted. My implementation runs efficiently based on the total iteration count, ranging from 180 to 280 when sending the text of John F. Kennedy’s Moon Speech. 
</div>
<br />

To run the code, run: `python3 .\rdt_main.py` in your terminal.
