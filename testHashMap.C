#include <map>
#include <iostream>
std::map<uint, std::map<uint, std::vector<unsigned long long> > > eventMap;


ushort findEvent(uint run, uint lumiBlock, unsigned long long event) {
  std::map<uint, std::map<uint, std::vector<unsigned long long> > >::iterator runIt = eventMap.find(run);
  if (runIt != eventMap.end()) {
    std::map<uint, std::vector<unsigned long long> >::iterator lumiIt = eventMap.at(run).find(lumiBlock);
    if (lumiIt != eventMap.at(run).end()) {

      if (std::find(eventMap.at(run).at(lumiBlock).begin(), eventMap.at(run).at(lumiBlock).end(), event) != eventMap.at(run).at(lumiBlock).end()) {
        return 0;    // found the event
      }
      else return 1; // found the run and lumiblock, but the event wasn't there
    }
    else return 2;   // found the run, but lumiblock wasn't there
  }
  else return 3;     // didn't find the run
}


void addEvent(uint run, uint lumiBlock, unsigned long long event) {
  ushort searchResult = findEvent(run, lumiBlock, event);
  if (searchResult==0) {
    std::cout << "Error! Trying to add an event that is already present!" << endl; 
  }  
  else if (searchResult == 1) {
    eventMap.at(run).at(lumiBlock).push_back(event);
  }
  else if (searchResult == 2) {
    std::vector<unsigned long long> newLumiBlock;
    newLumiBlock.push_back(event);
    eventMap.at(run).insert(std::pair<uint, std::vector<unsigned long long> >(lumiBlock, newLumiBlock));
  }
  else if (searchResult == 3) {
    std::map<uint, std::vector<unsigned long long> > newRun;
    std::vector<unsigned long long> newLumiBlock;
    newLumiBlock.push_back(event);
    newRun.insert(std::pair<uint, std::vector<unsigned long long> >(lumiBlock, newLumiBlock));
    eventMap.insert(std::pair<uint, std::map<uint, std::vector<unsigned long long> > >(run, newRun));
  }
}

void testHashMap() { 
  std::cout << "adding 123456:100:999999999" << std::endl;
  addEvent(123456, 100, 999999999);
  std::cout << "looking for 123456:100:999999999" << std::endl;
  std::cout << findEvent(123456, 100, 999999999) << std::endl;
  std::cout << "looking for 654321:200:888888888" << std::endl;
  std::cout << findEvent(654321, 200, 888888888) << std::endl;
  std::cout << "looking for 123456:200:888888888" << std::endl;
  std::cout << findEvent(123456, 200, 888888888) << std::endl;
  std::cout << "looking for 123456:100:888888888" << std::endl;
  std::cout << findEvent(123456, 100, 888888888) << std::endl;
  std::cout << "adding 123456:100:888888888" << std::endl;
  addEvent(123456, 100, 888888888);
  std::cout << "looking for 123456:100:888888888" << std::endl;
  std::cout << findEvent(123456, 100, 888888888) << std::endl;
}
