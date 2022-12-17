using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IktusApp.Models
{
  internal class ECG
  {
    public DateTime Date { get; set; }
    public FileInfo CSVFile { get; set; }

    // Fitbit or AppleWatch
    public string Type { get; set; }

  }
}
