<h1>Bitcoin-Core-vs-Bitcoin-Knots-Speed-Test</h1>
This script was made to take a clean look at ZMQ block propagation latency between Bitcoin Core and Bitcoin Knots running on my setup.<br> Specs: Ryzen 9 16/32 CPU, 24GB RAM, a 2TB and a 1TB m.2 nvme drives, half gig internet speed.<br><br>
Here is a breakdown of what this log tells us about how the two nodes are performing relative to each other:<br><br>

If we calculate the time difference (delta) for each block hash to see which node heard it first and by how many milliseconds, we get the following:<br>

<b>Core is dominant:</b> Out of the 10 blocks captured, Bitcoin Core won 9 times.<br>

<b>Average Propagation Delta:</b> When Core won, it received the block an average of 417 milliseconds before Knots.<br>

<b>The Outliers:</b> The last block before ten o'clock (...fc30b) saw a massive 999 ms gap, almost a full second, in Core's favor. On the flip side, Knots managed to scoop Core on the very first block by 167 ms.<br>

<img width="1027" height="619" alt="msblockmonitor" src="https://github.com/user-attachments/assets/2e7406fa-62b2-4b95-86b4-02eabc2b3b5d" /><br>

<b>Why the difference?</b><br><br>
Because Bitcoin Knots is a derivative of Bitcoin Core, their internal block validation mechanics are nearly identical. This latency disparity almost certainly comes down to peer-to-peer (P2P) networking topology:<br>

Peer Connections: The Bitcoin Core node likely has a connection to a peer (or a mining pool node) that is geographically closer, has higher bandwidth, or is closer to the miner who discovered the block.<br>

Compact Block Relaying (BIP152): Core is successfully reconstructing the blocks faster because it received the cmpctblock message first, or because its mempool was a more perfect match for the transactions in the block, requiring fewer round-trips to fetch missing transactions.<br>

Here is the data copied/pasted from the terminal to use in AI:<br>

btc@btc:~$ python3 msblockmonitor.py<br>
Listening for ZMQ block hashes down to the millisecond...<br>
[09:05:12.274] KNOTS ZMQ: New Block 00000000000000000000be41b3e1566fa65b917c85715db3244216139db92497<br>
[09:05:12.441] CORE ZMQ: New Block 00000000000000000000be41b3e1566fa65b917c85715db3244216139db92497<br>
[09:07:01.183] CORE ZMQ: New Block 00000000000000000000684505b41ce8dcf71ee21cf380c3643c04f10c08698a<br>
[09:07:01.402] KNOTS ZMQ: New Block 00000000000000000000684505b41ce8dcf71ee21cf380c3643c04f10c08698a<br>
[09:09:03.730] CORE ZMQ: New Block 0000000000000000000086695e5533861e58eb0f47ce95e83272df61be8e4b9d<br>
[09:09:03.967] KNOTS ZMQ: New Block 0000000000000000000086695e5533861e58eb0f47ce95e83272df61be8e4b9d<br>
[09:14:49.899] CORE ZMQ: New Block 000000000000000000012c6f0077f2ae9583cb16e169858d1a7c9ac9216c45c6<br>
[09:14:50.533] KNOTS ZMQ: New Block 000000000000000000012c6f0077f2ae9583cb16e169858d1a7c9ac9216c45c6<br>
[09:18:18.018] CORE ZMQ: New Block 00000000000000000001cea3ef906ba87a5f3ad6f40b311c12d2da1d3e00dd2f<br>
[09:18:18.525] KNOTS ZMQ: New Block 00000000000000000001cea3ef906ba87a5f3ad6f40b311c12d2da1d3e00dd2f<br>
[09:31:27.752] CORE ZMQ: New Block 000000000000000000008a54f395c5639fa67a3b77c28349a075ea1b2767433d<br>
[09:31:28.012] KNOTS ZMQ: New Block 000000000000000000008a54f395c5639fa67a3b77c28349a075ea1b2767433d<br>
[09:37:57.006] CORE ZMQ: New Block 0000000000000000000202438212971004e4d302788508e6c706e312548c6313<br>
[09:37:57.386] KNOTS ZMQ: New Block 0000000000000000000202438212971004e4d302788508e6c706e312548c6313<br>
[09:51:35.492] CORE ZMQ: New Block 00000000000000000000a51ba7756ec227d5c69707183f61aa88d54c67596778<br>
[09:51:35.781] KNOTS ZMQ: New Block 00000000000000000000a51ba7756ec227d5c69707183f61aa88d54c67596778<br>
[09:54:10.092] CORE ZMQ: New Block 00000000000000000000d19f25052d2bf029fa98fa8c1ad8bf1dfe4ba9dfc30b<br>
[09:54:11.091] KNOTS ZMQ: New Block 00000000000000000000d19f25052d2bf029fa98fa8c1ad8bf1dfe4ba9dfc30b<br>
[10:01:54.307] CORE ZMQ: New Block 000000000000000000005c941133f74069c363a21b8c9ad27e9fec8e68baa195<br>
[10:01:54.535] KNOTS ZMQ: New Block 000000000000000000005c941133f74069c363a21b8c9ad27e9fec8e68baa195<br>
[10:22:05.205] CORE ZMQ: New Block 00000000000000000000aa2dc1715a5c6875af0ce31e04c76a3c7c76d814eaef<br>
[10:22:05.637] KNOTS ZMQ: New Block 00000000000000000000aa2dc1715a5c6875af0ce31e04c76a3c7c76d814eaef<br>
[10:30:50.866] CORE ZMQ: New Block 00000000000000000001851731982bfdf47d5858832ebc284f9dc14957b8d111<br>
[10:30:51.372] KNOTS ZMQ: New Block 00000000000000000001851731982bfdf47d5858832ebc284f9dc14957b8d111<br>
[11:20:22.944] CORE ZMQ: New Block 00000000000000000001450de9bc279d6c0967ec15d67defa4269f2c52aa3b48<br>
[11:20:23.103] KNOTS ZMQ: New Block 00000000000000000001450de9bc279d6c0967ec15d67defa4269f2c52aa3b48<br><br>

<b>To use the script, make sure to change IPC file path for both subscriber!</b>  
<br>

<h4>Donations are highly appreciated and can be made via crypto:</h4>
<b>DGB</b> wallet address:&nbsp;&nbsp;DEkZrJo1BHdiqnQq1XQSWGymEcDWGAWwZs<br>
<b>DOGE</b> wallet address:&nbsp;&nbsp;DKZ9sv4VoTiQQdwi7VY25573UfpQqZJfYf<br>
<b>LTC</b> wallet address:&nbsp;&nbsp;MJw3XHpR65Ec8rKEBthK5Dnvcy1CixYGTa<br>
<b>BCH</b> wallet address:&nbsp;&nbsp;bitcoincash:qq66dg3vhczrqf4zy4kxje3c45vz47khsufsludxcc<br><br>
Thank you.
<br><br>
