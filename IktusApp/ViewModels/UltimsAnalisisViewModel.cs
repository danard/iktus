using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using CommunityToolkit.Mvvm.Messaging;
using IktusApp.Messages;
using IktusApp.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IktusApp.ViewModels
{
  internal partial class UltimsAnalisisViewModel : ObservableObject, IRecipient<MessageManager>
  {
    public UltimsAnalisisViewModel()
    {
      WeakReferenceMessenger.Default.Register<MessageManager>(this);
    }


    [ObservableProperty]
    List<ECG> _listAnalysis;

    public void AddECG(ECG ecG)
    {
      if (ListAnalysis == null)
      {
        ListAnalysis = new List<ECG>();
      }
      ListAnalysis.Add(ecG);
    }

    [RelayCommand]
    public static async Task OpenPDFFile(FileInfo item)
    {
      string filePath = item.FullName;
      await Launcher.Default.OpenAsync(new OpenFileRequest("Electrocardiograma", new ReadOnlyFile(filePath)));
    }

    public void Receive(MessageManager message)
    {
      MainThread.BeginInvokeOnMainThread(() =>
      {
        AddECG(message.Value);
      });
    }
  }
}
