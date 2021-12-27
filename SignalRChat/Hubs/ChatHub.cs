using System;
using Microsoft.AspNetCore.SignalR;

namespace SignalRChat.Hubs
{
	public class ChatHub : Hub
	{
		public ChatHub()
		{

		}
		// represent the calculation as an int
		private static Dictionary<string, int> Calculation = new Dictionary<string, int>();

		public async Task SendMessage(string user, string message)
		{
			await Clients.All.SendAsync("ReceiveMessage", user, message);
		}

		public async Task StartCalculation(string user, string message)
		{
			var id = Context.ConnectionId;
			if (!Calculation.TryAdd(id, 1))
				Calculation[id] = 1;
			await Clients.Caller.SendAsync("ReceiveMessage", "system", "started calculation");
			Thread.Sleep(2000);
			await Clients.Caller.SendAsync("NeedMoreData", "system", "mid calculation");
		}
		public async Task ContinueCalculation(string data)
		{
			var id = Context.ConnectionId;
			await Clients.Caller.SendAsync("ReceiveMessage", "system", "continuing calculation");
			Thread.Sleep(2000);
			if (Calculation[id]++ < 4)
				await Clients.Caller.SendAsync("NeedMoreData", "system", "mid calculation");
			else 
				await Clients.Caller.SendAsync("FinishedCalculation", "result");
		}
	}
}

