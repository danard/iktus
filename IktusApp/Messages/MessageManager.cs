
using CommunityToolkit.Mvvm.Messaging.Messages;
using IktusApp.Models;

namespace IktusApp.Messages
{
  internal class MessageManager : ValueChangedMessage<ECG>
  {
    public MessageManager(ECG value) : base(value)
    {
    }
  }
}
