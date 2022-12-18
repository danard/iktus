using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using CommunityToolkit.Mvvm.Messaging;
using CommunityToolkit.Mvvm.Messaging.Messages;
using IktusApp.Messages;
using IktusApp.Models;
using IktusApp.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IktusApp.ViewModels
{
  public partial class ECGViewModel : ObservableObject
  {
    [ObservableProperty]
    bool _isLoading = false;

    [ObservableProperty]
    string _lastResult = null;

    private ECG GetRandomECG()
    {
      int id = new Random().Next(1, 5);
      var test = new FileInfo(Path.Combine("C:\\Users\\ardevold\\Downloads\\Ictus Files\\EGC Files\\" + $"ecg{id}.pdf"));

      return new ECG
        (
        DateTime.Now,
        test,
        "FitBit"
        );
    }

    [RelayCommand]
    public async Task SendNewAnalysis()
    {
      IsLoading = true;
      try
      {
        var ecg = GetRandomECG();

        WeakReferenceMessenger.Default.Send(new MessageManager(ecg));

        LastResult = await RestService.SendNewECG(ecg);
      }
      finally
      {
        IsLoading = false;
      }
    }
  }
}
